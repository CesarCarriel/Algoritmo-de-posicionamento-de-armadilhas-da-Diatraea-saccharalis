"""
***************************************************************************
*                                                                         *
*   Este script é proprietário e não é de código aberto.                  *
*   Direitos autorais reservados ao desenvolvedor.                        *
*                                                                         *
*   Desenvolvedor: João Silva                                             *
*   Data de desenvolvimento: 11 de outubro de 2024                        *
*   Contato: cesarcarrieldev@gmail.com                                    *
*                                                                         *
*   Uso ou redistribuição deste código só é permitido com autorização     *
*   explícita do desenvolvedor.                                           *
*                                                                         *
***************************************************************************
"""

import math

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing, QgsFeatureSink, QgsProcessingException, QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource, QgsProcessingParameterFeatureSink, QgsVectorLayer, QgsField,
                       QgsGeometry, QgsWkbTypes, QgsFeature)
from qgis.processing import run


class DiatraeaSaccharalisMonitoringTrapPositioningOptimizationAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DiatraeaSaccharalisMonitoringTrapPositioningOptimizationAlgorithm()

    def name(self):
        return 'diatraeasaccharalismonitoringtrappositioningoptimizationalgorithm'

    def displayName(self):
        return self.tr('Diatraea saccharalis Monitoring Trap Positioning Optimization')

    def group(self):
        return self.tr('Sugar cane')

    def groupId(self):
        return 'sugarcane'

    def shortHelpString(self):
        return self.tr(
            """
            Este algoritmo realiza a otimização espacial do posicionamento de armadilhas para o monitoramento de Diatraea saccharalis.
            
            Desenvolvido por: César Santos Carriel
            LinkedIn: https://www.linkedin.com/in/cesarcarriel/
            
            Este script é proprietário. Direitos reservados.
            """
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.SourceType.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def calcular_numero_necessario_de_armadilhas(self, layer, hectares_por_armadilha):
        total_area = 0

        for feature in layer.getFeatures():
            geom = feature.geometry()
            area = geom.area()

            total_area += area

        total_area_ha = total_area / 10000
        numero_de_armadilhas = math.ceil(total_area_ha / hectares_por_armadilha)

        return numero_de_armadilhas

    def criar_contorno_dos_talhoes(self, layer):
        buffer_params = {
            'INPUT': layer,
            'DISTANCE': 10,
            'SEGMENTS': 5,
            'DISSOLVE': False,
            'OUTPUT': 'memory:buffer_positivo'
        }
        buffer_layer = run("native:buffer", buffer_params)['OUTPUT']

        dissolve_params = {
            'INPUT': buffer_layer,
            'OUTPUT': 'memory:dissolve'
        }
        dissolved_layer = run("native:dissolve", dissolve_params)['OUTPUT']

        buffer_neg_params = {
            'INPUT': dissolved_layer,
            'DISTANCE': -5,
            'SEGMENTS': 5,
            'DISSOLVE': False,
            'OUTPUT': 'memory:buffer_negativo'
        }
        buffer_neg_layer = run("native:buffer", buffer_neg_params)['OUTPUT']

        return buffer_neg_layer

    def calcular_a_abrangencia_de_cada_possivel_armadilha_a_volta_dos_talhoes(self, layer):
        polygon_to_line_params = {
            'INPUT': layer,
            'OUTPUT': 'memory:polygon_to_line'
        }
        line_layer = run("native:polygonstolines", polygon_to_line_params)['OUTPUT']

        split_lines_params = {
            'INPUT': line_layer,
            'LENGTH': 5,
            'OUTPUT': 'memory:split_lines'
        }
        split_line_layer = run("native:splitlinesbylength", split_lines_params)['OUTPUT']

        points_params = {
            'INPUT': split_line_layer,
            'DISTANCE': 5,
            'OUTPUT': 'memory:centroid_points'
        }

        pontos_ao_longo_da_borda_do_poligono = run("native:pointsalonglines", points_params)['OUTPUT']

        buffer_raio = 398.94245

        buffer_params = {
            'INPUT': pontos_ao_longo_da_borda_do_poligono,
            'DISTANCE': buffer_raio,
            'SEGMENTS': 50,
            'DISSOLVE': False,
            'OUTPUT': 'memory:buffer'
        }

        area_de_cada_ponto = run("native:buffer", buffer_params)['OUTPUT']

        return area_de_cada_ponto

    def lista_locais_para_instalacao_das_armadilhas_na_area(self, layer):
        contorno_dos_talhoes = self.criar_contorno_dos_talhoes(layer)
        contorno_dos_talhoes_geom = QgsGeometry.unaryUnion(
            [feature.geometry() for feature in contorno_dos_talhoes.getFeatures()])

        abrangencia_de_cada_possivel_armadilha = self.calcular_a_abrangencia_de_cada_possivel_armadilha_a_volta_dos_talhoes(
            layer)

        crs = abrangencia_de_cada_possivel_armadilha.crs()
        centroid_layer = QgsVectorLayer("Point?crs={}".format(crs.authid()), "Centroides", "memory")
        centroid_layer_data = centroid_layer.dataProvider()

        centroid_layer_data.addAttributes([QgsField('area_ha', QVariant.Double)])
        centroid_layer.updateFields()

        posicao_das_armadilhas_com_maior_area_de_abrangencia_layer = QgsVectorLayer(
            "Polygon?crs={}".format(crs.authid()),
            "Interseções", "memory")
        posicao_das_armadilhas_com_maior_area_de_abrangencia_layer_data = posicao_das_armadilhas_com_maior_area_de_abrangencia_layer.dataProvider()

        posicao_das_armadilhas_com_maior_area_de_abrangencia_layer_data.addAttributes(
            [QgsField('area_ha', QVariant.Double)])
        posicao_das_armadilhas_com_maior_area_de_abrangencia_layer.updateFields()

        numero_necessario_de_armadilhas = self.calcular_numero_necessario_de_armadilhas(layer, 50)

        for i in range(numero_necessario_de_armadilhas):
            largest_feature = None
            largest_area_ha = 0
            original_feature_for_centroid = None

            for feature in abrangencia_de_cada_possivel_armadilha.getFeatures():
                geom1 = feature.geometry()

                if geom1.intersects(contorno_dos_talhoes_geom):
                    intersection = geom1.intersection(contorno_dos_talhoes_geom)

                    if not intersection.isEmpty():
                        area_ha = intersection.area() / 10000

                        if area_ha > largest_area_ha:
                            largest_area_ha = area_ha
                            largest_feature = QgsFeature()
                            largest_feature.setGeometry(intersection)
                            largest_feature.setAttributes([area_ha])
                            original_feature_for_centroid = feature

            if largest_feature:
                posicao_das_armadilhas_com_maior_area_de_abrangencia_layer_data.addFeature(largest_feature)

                centroid_geom = original_feature_for_centroid.geometry().centroid()
                centroid_feature = QgsFeature()
                centroid_feature.setGeometry(centroid_geom)
                centroid_feature.setAttributes([largest_area_ha])

                centroid_layer_data.addFeature(centroid_feature)

                contorno_dos_talhoes_geom = contorno_dos_talhoes_geom.difference(largest_feature.geometry())

        return centroid_layer

    def processAlgorithm(self, parameters, context, feedback):
        try:
            source = self.parameterAsSource(parameters, self.INPUT, context)

            if source is None:
                raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

            point_wkb_type = QgsWkbTypes.Point  # Ou QgsWkbTypes.MultiPoint se necessário

            (sink, dest_id) = self.parameterAsSink(
                parameters,
                self.OUTPUT,
                context,
                source.fields(),
                point_wkb_type,
                source.sourceCrs()
            )

            if sink is None:
                raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

            total = 100.0 / source.featureCount() if source.featureCount() else 0

            source_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)

            try:
                locais_das_armadilhas = self.lista_locais_para_instalacao_das_armadilhas_na_area(source_layer)

            except Exception as e:
                feedback.reportError(f'Erro ao calcular os locais das armadilhas: {str(e)}')
                raise QgsProcessingException(f'Erro ao calcular os locais das armadilhas: {str(e)}')

            for current, feature in enumerate(locais_das_armadilhas.getFeatures()):
                if feedback.isCanceled():
                    break

                new_feature = QgsFeature()
                new_feature.setGeometry(feature.geometry())

                sink.addFeature(new_feature, QgsFeatureSink.Flag.FastInsert)
                feedback.setProgress(int(current * total))

            feedback.pushInfo(f'Processamento concluído com sucesso! CRS: {source.sourceCrs().authid()}')

        except Exception as e:
            feedback.reportError(f'Erro no algoritmo: {str(e)}', fatalError=True)
            raise QgsProcessingException(f'Erro inesperado: {str(e)}')

        return {self.OUTPUT: dest_id}
