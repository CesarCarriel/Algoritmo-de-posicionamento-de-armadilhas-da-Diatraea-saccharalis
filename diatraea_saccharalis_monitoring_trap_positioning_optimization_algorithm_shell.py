from qgis.processing import run


def calculate_required_number_of_traps(layer, hectares_per_trap):
    total_area = 0

    for feature in layer.getFeatures():
        geom = feature.geometry()
        total_area += geom.area()

    total_area_ha = total_area / 10000

    required_number_of_traps = math.ceil(total_area_ha / hectares_per_trap)

    return required_number_of_traps


def create_contour_of_talhoes(layer):
    buffer_params = dict(
        INPUT=layer,
        DISTANCE=10,
        SEGMENTS=5,
        DISSOLVE=False,
        OUTPUT='memory:positive_buffer'
    )
    buffer_layer = run('native:buffer', buffer_params)['OUTPUT']

    dissolve_params = dict(
        INPUT=buffer_layer,
        OUTPUT='memory:dissolve'
    )
    dissolved_layer = run('native:dissolve', dissolve_params)['OUTPUT']

    buffer_negative_params = dict(
        INPUT=dissolved_layer,
        DISTANCE=-5,
        SEGMENTS=5,
        DISSOLVE=False,
        OUTPUT='memory:negative_buffer'
    )
    buffer_negative_layer = run('native:buffer', buffer_negative_params)['OUTPUT']

    return buffer_negative_layer


def calculate_the_coverage_of_each_possible_trap_on_the_edge_of_the_talhoes(layer):
    polygon_to_line_params = dict(
        INPUT=layer,
        OUTPUT='memory:polygon_to_line'
    )
    line_layer = run('native:polygonstolines', polygon_to_line_params)['OUTPUT']

    split_lines_params = dict(
        INPUT=line_layer,
        LENGTH=50,
        OUTPUT='memory:split_lines'
    )
    split_line_layer = run('native:splitlinesbylength', split_lines_params)['OUTPUT']

    points_params = dict(
        INPUT=split_line_layer,
        DISTANCE=50,
        OUTPUT='memory:centroid_points'
    )

    points_along_the_edge_of_the_polygon = run('native:pointsalonglines', points_params)['OUTPUT']

    buffer_radius_to_create_polygon_of_50_hectares = 398.94245

    buffer_params = dict(
        INPUT=points_along_the_edge_of_the_polygon,
        DISTANCE=buffer_radius_to_create_polygon_of_50_hectares,
        SEGMENTS=50,
        DISSOLVE=False,
        OUTPUT='memory:buffer'
    )

    coverage_area_of_each_trap = run('native:buffer', buffer_params)['OUTPUT']

    return coverage_area_of_each_trap


def points_for_trap_installation_in_the_area(layer):
    contour_of_the_plots = create_contour_of_talhoes(layer)
    contour_of_the_plots_geom = QgsGeometry.unaryUnion(
        [feature.geometry() for feature in contour_of_the_plots.getFeatures()]
    )

    coverage_of_each_possible_trap = calculate_the_coverage_of_each_possible_trap_on_the_edge_of_the_talhoes(layer)
    coverage_of_each_possible_trap_data = coverage_of_each_possible_trap .dataProvider()

    crs = coverage_of_each_possible_trap.crs()
    trap_points = QgsVectorLayer('Point?crs={}'.format(crs.authid()), 'Posição das armadilhas', 'memory')
    traps_data = trap_points.dataProvider()

    traps_data.addAttributes([QgsField('area_ha', QVariant.Double)])
    trap_points.updateFields()

    traps_with_the_greatest_coverage_in_the_area_layer = QgsVectorLayer(
        'Polygon?crs={}'.format(crs.authid()), 'Coverage das armadilhas', 'memory'
    )
    traps_with_the_greatest_coverage_in_the_area_layer_data = traps_with_the_greatest_coverage_in_the_area_layer .dataProvider()

    traps_with_the_greatest_coverage_in_the_area_layer_data.addAttributes([QgsField('area_ha', QVariant.Double)])
    traps_with_the_greatest_coverage_in_the_area_layer.updateFields()

    required_number_of_traps = calculate_required_number_of_traps(layer, 50)

    for i in range(required_number_of_traps):
        largest_feature = None
        largest_area_ha = 0
        original_feature_for_centroid = None

        for feature in coverage_of_each_possible_trap.getFeatures():
            coverage_trap = feature.geometry()

            if coverage_trap.intersects(contour_of_the_plots_geom):
                effective_coverage_of_the_trap = coverage_trap.intersection(contour_of_the_plots_geom)

                if not effective_coverage_of_the_trap.isEmpty():
                    area_ha = effective_coverage_of_the_trap.area() / 10000

                    if area_ha > largest_area_ha:
                        largest_area_ha = area_ha
                        largest_feature = QgsFeature()
                        largest_feature.setGeometry(effective_coverage_of_the_trap)
                        largest_feature.setAttributes([area_ha])
                        original_feature_for_centroid = feature

                    if round(coverage_trap.area() / 10000, 2) == round(area_ha, 2):
                        break

        if largest_feature:
            traps_with_the_greatest_coverage_in_the_area_layer_data.addFeature(largest_feature)

            for feature_trap in coverage_of_each_possible_trap_data.getFeatures():
                centroid_trap = feature_trap.geometry().centroid()

                if centroid_trap.intersects(largest_feature.geometry()):
                    coverage_of_each_possible_trap_data.deleteFeatures([feature_trap.id()])

            coverage_of_each_possible_trap.triggerRepaint()

            QgsProject.instance().addMapLayer(traps_with_the_greatest_coverage_in_the_area_layer)

            centroid_geom = original_feature_for_centroid.geometry().centroid()
            centroid_feature = QgsFeature()
            centroid_feature.setGeometry(centroid_geom)
            centroid_feature.setAttributes([largest_area_ha])

            traps_data.addFeature(centroid_feature)

            contour_of_the_plots_geom = contour_of_the_plots_geom.difference(largest_feature.geometry())

    return trap_points


layer = iface.activeLayer()

trap_points = points_for_trap_installation_in_the_area(layer)
QgsProject.instance().addMapLayer(trap_points)

print(f'Segue os melhores pontos para a instalação das armadilhas da Diatraeae Saccharalis.')
