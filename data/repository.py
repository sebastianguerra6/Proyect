import json
import os
from typing import List, Dict, Any, Optional
from models import Onboarding, Offboarding, LateralMovement

class EmpleadoRepository:
    """Clase para manejar el almacenamiento y recuperación de datos de empleados"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Asegura que el directorio de datos existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _get_file_path(self, tipo_proceso: str) -> str:
        """Obtiene la ruta del archivo para un tipo de proceso"""
        return os.path.join(self.data_dir, f"datos_empleados_{tipo_proceso}.json")
    
    def guardar_onboarding(self, onboarding: Onboarding) -> bool:
        """Guarda un proceso de onboarding"""
        return self._guardar_proceso(onboarding, "onboarding")
    
    def guardar_offboarding(self, offboarding: Offboarding) -> bool:
        """Guarda un proceso de offboarding"""
        return self._guardar_proceso(offboarding, "offboarding")
    
    def guardar_lateral_movement(self, lateral: LateralMovement) -> bool:
        """Guarda un proceso de lateral movement"""
        return self._guardar_proceso(lateral, "lateral")
    
    def _guardar_proceso(self, proceso, tipo_proceso: str) -> bool:
        """Método privado para guardar cualquier tipo de proceso"""
        try:
            archivo = self._get_file_path(tipo_proceso)
            datos_existentes = self._cargar_datos_existentes(archivo)
            
            datos_existentes.append(proceso.to_dict())
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_existentes, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar {tipo_proceso}: {str(e)}")
            return False
    
    def _cargar_datos_existentes(self, archivo: str) -> List[Dict[str, Any]]:
        """Carga datos existentes de un archivo"""
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def cargar_onboardings(self) -> List[Onboarding]:
        """Carga todos los procesos de onboarding"""
        return self._cargar_procesos("onboarding", Onboarding)
    
    def cargar_offboardings(self) -> List[Offboarding]:
        """Carga todos los procesos de offboarding"""
        return self._cargar_procesos("offboarding", Offboarding)
    
    def cargar_lateral_movements(self) -> List[LateralMovement]:
        """Carga todos los procesos de lateral movement"""
        return self._cargar_procesos("lateral", LateralMovement)
    
    def _cargar_procesos(self, tipo_proceso: str, clase_proceso) -> List:
        """Método privado para cargar cualquier tipo de proceso"""
        try:
            archivo = self._get_file_path(tipo_proceso)
            datos = self._cargar_datos_existentes(archivo)
            
            procesos = []
            for dato in datos:
                try:
                    proceso = clase_proceso.from_dict(dato)
                    procesos.append(proceso)
                except Exception as e:
                    print(f"Error al cargar proceso {tipo_proceso}: {str(e)}")
                    continue
            
            return procesos
        except Exception as e:
            print(f"Error al cargar {tipo_proceso}: {str(e)}")
            return []
    
    def obtener_estadisticas(self) -> Dict[str, int]:
        """Obtiene estadísticas de los datos almacenados"""
        return {
            "onboarding": len(self.cargar_onboardings()),
            "offboarding": len(self.cargar_offboardings()),
            "lateral": len(self.cargar_lateral_movements())
        }
