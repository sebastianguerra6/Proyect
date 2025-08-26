import json
import os
from typing import List, Dict, Any, Optional
from models import Onboarding, Offboarding, LateralMovement, PersonaHeadcount

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
    
    def _get_headcount_file_path(self) -> str:
        """Obtiene la ruta del archivo de headcount"""
        return os.path.join(self.data_dir, "headcount.json")
    
    def guardar_onboarding(self, onboarding: Onboarding) -> bool:
        """Guarda un proceso de onboarding"""
        return self._guardar_proceso(onboarding, "onboarding")
    
    def guardar_offboarding(self, offboarding: Offboarding) -> bool:
        """Guarda un proceso de offboarding"""
        return self._guardar_proceso(offboarding, "offboarding")
    
    def guardar_lateral_movement(self, lateral: LateralMovement) -> bool:
        """Guarda un proceso de lateral movement"""
        return self._guardar_proceso(lateral, "lateral")
    
    def guardar_persona_headcount(self, persona: PersonaHeadcount) -> bool:
        """Guarda una persona en el headcount"""
        try:
            archivo = self._get_headcount_file_path()
            datos_existentes = self._cargar_headcount_existente()
            
            datos_existentes.append(persona.to_dict())
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_existentes, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar persona en headcount: {str(e)}")
            return False
    
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
    
    def _cargar_headcount_existente(self) -> List[Dict[str, Any]]:
        """Carga datos existentes del headcount"""
        return self._cargar_datos_existentes(self._get_headcount_file_path())
    
    def buscar_por_sid(self, sid: str) -> List[Dict[str, Any]]:
        """Busca registros por SID en todos los tipos de procesos"""
        if not sid.strip():
            return []
        
        resultados = []
        sid_buscar = sid.strip()
        
        # Buscar en onboarding
        try:
            with open(self._get_file_path("onboarding"), 'r', encoding='utf-8') as f:
                datos_onboarding = json.load(f)
                for proceso in datos_onboarding:
                    if proceso.get('empleado', {}).get('sid', '').strip() == sid_buscar:
                        resultado = proceso.copy()
                        resultado['tipo_proceso'] = 'Onboarding'
                        resultados.append(resultado)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Buscar en offboarding
        try:
            with open(self._get_file_path("offboarding"), 'r', encoding='utf-8') as f:
                datos_offboarding = json.load(f)
                for proceso in datos_offboarding:
                    if proceso.get('empleado', {}).get('sid', '').strip() == sid_buscar:
                        resultado = proceso.copy()
                        resultado['tipo_proceso'] = 'Offboarding'
                        resultados.append(resultado)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Buscar en lateral movement
        try:
            with open(self._get_file_path("lateral"), 'r', encoding='utf-8') as f:
                datos_lateral = json.load(f)
                for proceso in datos_lateral:
                    if proceso.get('empleado', {}).get('sid', '').strip() == sid_buscar:
                        resultado = proceso.copy()
                        resultado['tipo_proceso'] = 'Lateral Movement'
                        resultados.append(resultado)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        return resultados
    
    def buscar_por_numero_caso(self, numero_caso: str) -> List[Dict[str, Any]]:
        """Busca registros por número de caso en todos los tipos de procesos"""
        if not numero_caso.strip():
            return []
        
        resultados = []
        caso_buscar = numero_caso.strip()
        
        # Buscar en onboarding
        try:
            with open(self._get_file_path("onboarding"), 'r', encoding='utf-8') as f:
                datos_onboarding = json.load(f)
                for proceso in datos_onboarding:
                    if proceso.get('empleado', {}).get('numero_caso', '').strip() == caso_buscar:
                        resultado = proceso.copy()
                        resultado['tipo_proceso'] = 'Onboarding'
                        resultados.append(resultado)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Buscar en offboarding
        try:
            with open(self._get_file_path("offboarding"), 'r', encoding='utf-8') as f:
                datos_offboarding = json.load(f)
                for proceso in datos_offboarding:
                    if proceso.get('empleado', {}).get('numero_caso', '').strip() == caso_buscar:
                        resultado = proceso.copy()
                        resultado['tipo_proceso'] = 'Offboarding'
                        resultados.append(resultado)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Buscar en lateral movement
        try:
            with open(self._get_file_path("lateral"), 'r', encoding='utf-8') as f:
                datos_lateral = json.load(f)
                for proceso in datos_lateral:
                    if proceso.get('empleado', {}).get('numero_caso', '').strip() == caso_buscar:
                        resultado = proceso.copy()
                        resultado['tipo_proceso'] = 'Lateral Movement'
                        resultados.append(resultado)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        return resultados
    
    def cargar_onboardings(self) -> List[Onboarding]:
        """Carga todos los procesos de onboarding"""
        return self._cargar_procesos("onboarding", Onboarding)
    
    def cargar_offboardings(self) -> List[Offboarding]:
        """Carga todos los procesos de offboarding"""
        return self._cargar_procesos("offboarding", Offboarding)
    
    def cargar_lateral_movements(self) -> List[LateralMovement]:
        """Carga todos los procesos de lateral movement"""
        return self._cargar_procesos("lateral", LateralMovement)
    
    def cargar_personas_headcount(self) -> List[PersonaHeadcount]:
        """Carga todas las personas del headcount"""
        try:
            archivo = self._get_headcount_file_path()
            datos = self._cargar_headcount_existente()
            
            personas = []
            for dato in datos:
                try:
                    persona = PersonaHeadcount.from_dict(dato)
                    personas.append(persona)
                except Exception as e:
                    print(f"Error al cargar persona del headcount: {str(e)}")
                    continue
            
            return personas
        except Exception as e:
            print(f"Error al cargar headcount: {str(e)}")
            return []
    
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
            "lateral": len(self.cargar_lateral_movements()),
            "headcount": len(self.cargar_personas_headcount())
        }
