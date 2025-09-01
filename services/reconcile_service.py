"""
Servicio de conciliación de accesos
"""
from typing import Dict, List, Any, Tuple
from datetime import datetime
from db.queries import reconciliation_queries
from db.connection import execute_update


class ReconciliationService:
    """Servicio para conciliar accesos de usuarios"""
    
    def __init__(self):
        self.queries = reconciliation_queries
    
    def reconcile_person(self, sid: str) -> Dict[str, Any]:
        """
        Concilia los accesos de una persona específica
        
        Returns:
            Dict con estructura:
            {
                "current": [{"app_name": "...", "role_name": "..."}],
                "target": [{"app_name": "...", "role_name": "..."}],
                "to_grant": [{"sid": sid, "app_name": "...", "accion": "GRANT", "motivo": "..."}],
                "to_revoke": [{"sid": sid, "app_name": "...", "accion": "REVOKE", "motivo": "..."}]
            }
        """
        try:
            # Verificar que la persona existe
            person_info = self.queries.get_person_info(sid)
            if not person_info:
                return {
                    "error": f"Persona con SID {sid} no encontrada",
                    "current": [],
                    "target": [],
                    "to_grant": [],
                    "to_revoke": []
                }
            
            # Obtener accesos actuales
            current_accesses = self.queries.get_current_accesses(sid)
            current_formatted = [
                {"app_name": row[0], "role_name": row[1]} 
                for row in current_accesses
            ]
            
            # Obtener accesos objetivo
            target_accesses = self.queries.get_target_accesses(sid)
            target_formatted = [
                {"app_name": row[0], "role_name": row[1]} 
                for row in target_accesses
            ]
            
            # Obtener accesos a otorgar
            to_grant_raw = self.queries.get_accesses_to_grant(sid)
            to_grant_formatted = [
                {
                    "sid": sid,
                    "app_name": row[0],
                    "role_name": row[1],
                    "accion": row[2],
                    "motivo": row[3]
                }
                for row in to_grant_raw
            ]
            
            # Obtener accesos a revocar
            to_revoke_raw = self.queries.get_accesses_to_revoke(sid)
            to_revoke_formatted = [
                {
                    "sid": sid,
                    "app_name": row[0],
                    "role_name": row[1],
                    "accion": row[2],
                    "motivo": row[3]
                }
                for row in to_revoke_raw
            ]
            
            return {
                "current": current_formatted,
                "target": target_formatted,
                "to_grant": to_grant_formatted,
                "to_revoke": to_revoke_formatted
            }
            
        except Exception as e:
            return {
                "error": f"Error en conciliación: {str(e)}",
                "current": [],
                "target": [],
                "to_grant": [],
                "to_revoke": []
            }
    
    def reconcile_all(self) -> List[Dict[str, Any]]:
        """
        Concilia los accesos de todas las personas en el sistema
        
        Returns:
            Lista de resultados de conciliación por persona
        """
        try:
            all_persons = self.queries.get_all_persons()
            results = []
            
            for person in all_persons:
                sid = person[0]
                reconciliation_result = self.reconcile_person(sid)
                if "error" not in reconciliation_result:
                    reconciliation_result["person_info"] = {
                        "sid": person[0],
                        "area": person[1],
                        "subunit": person[2],
                        "cargo": person[3],
                        "email": person[4]
                    }
                results.append(reconciliation_result)
            
            return results
            
        except Exception as e:
            return [{"error": f"Error en conciliación masiva: {str(e)}"}]
    
    def get_reconciliation_summary(self, sid: str = None) -> Dict[str, Any]:
        """
        Obtiene un resumen de la conciliación
        
        Args:
            sid: SID específico o None para resumen general
            
        Returns:
            Dict con resumen de conciliación
        """
        try:
            if sid:
                # Resumen para una persona específica
                summary = self.queries.get_access_summary_by_sid(sid)
                person_info = self.queries.get_person_info(sid)
                
                if person_info:
                    summary["person"] = {
                        "sid": person_info[0][0],
                        "area": person_info[0][1],
                        "subunit": person_info[0][2],
                        "cargo": person_info[0][3]
                    }
                
                return summary
            else:
                # Resumen general del sistema
                all_persons = self.queries.get_all_persons()
                total_persons = len(all_persons)
                
                # Contar totales
                total_current = 0
                total_target = 0
                total_to_grant = 0
                total_to_revoke = 0
                
                for person in all_persons:
                    sid = person[0]
                    summary = self.queries.get_access_summary_by_sid(sid)
                    total_current += summary.get('current', 0)
                    total_target += summary.get('target', 0)
                    total_to_grant += summary.get('to_grant', 0)
                    total_to_revoke += summary.get('to_revoke', 0)
                
                return {
                    "total_persons": total_persons,
                    "total_current_accesses": total_current,
                    "total_target_accesses": total_target,
                    "total_to_grant": total_to_grant,
                    "total_to_revoke": total_to_revoke
                }
                
        except Exception as e:
            return {"error": f"Error obteniendo resumen: {str(e)}"}
    
    def validate_reconciliation_data(self, reconciliation_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Valida que los datos de conciliación sean correctos
        
        Args:
            reconciliation_data: Datos de conciliación a validar
            
        Returns:
            Tuple (is_valid, error_message)
        """
        try:
            required_keys = ["current", "target", "to_grant", "to_revoke"]
            
            for key in required_keys:
                if key not in reconciliation_data:
                    return False, f"Falta clave requerida: {key}"
                
                if not isinstance(reconciliation_data[key], list):
                    return False, f"La clave {key} debe ser una lista"
            
            # Validar estructura de to_grant y to_revoke
            for item in reconciliation_data["to_grant"]:
                if not all(k in item for k in ["sid", "app_name", "accion", "motivo"]):
                    return False, "Elemento en to_grant tiene estructura incorrecta"
                if item["accion"] != "GRANT":
                    return False, "Acción en to_grant debe ser 'GRANT'"
            
            for item in reconciliation_data["to_revoke"]:
                if not all(k in item for k in ["sid", "app_name", "accion", "motivo"]):
                    return False, "Elemento en to_revoke tiene estructura incorrecta"
                if item["accion"] != "REVOKE":
                    return False, "Acción en to_revoke debe ser 'REVOKE'"
            
            return True, ""
            
        except Exception as e:
            return False, f"Error en validación: {str(e)}"
    
    def get_reconciliation_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas detalladas de la conciliación
        
        Returns:
            Dict con estadísticas del sistema
        """
        try:
            # Estadísticas por subunidad
            matrix_summary = self.queries.get_authorized_matrix_summary()
            
            # Estadísticas de accesos
            all_persons = self.queries.get_all_persons()
            stats_by_subunit = {}
            
            for person in all_persons:
                sid = person[0]
                subunit = person[2]
                cargo = person[3]
                
                if subunit not in stats_by_subunit:
                    stats_by_subunit[subunit] = {
                        "total_persons": 0,
                        "cargos": set(),
                        "total_current": 0,
                        "total_target": 0,
                        "total_to_grant": 0,
                        "total_to_revoke": 0
                    }
                
                stats_by_subunit[subunit]["total_persons"] += 1
                stats_by_subunit[subunit]["cargos"].add(cargo)
                
                summary = self.queries.get_access_summary_by_sid(sid)
                stats_by_subunit[subunit]["total_current"] += summary.get('current', 0)
                stats_by_subunit[subunit]["total_target"] += summary.get('target', 0)
                stats_by_subunit[subunit]["total_to_grant"] += summary.get('to_grant', 0)
                stats_by_subunit[subunit]["total_to_revoke"] += summary.get('to_revoke', 0)
            
            # Convertir sets a listas para serialización JSON
            for subunit in stats_by_subunit:
                stats_by_subunit[subunit]["cargos"] = list(stats_by_subunit[subunit]["cargos"])
            
            return {
                "matrix_summary": matrix_summary,
                "stats_by_subunit": stats_by_subunit,
                "total_persons": len(all_persons)
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo estadísticas: {str(e)}"}


# Instancia global para usar en toda la aplicación
reconciliation_service = ReconciliationService()

