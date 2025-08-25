classDiagram
direction TB

class BaseApplication {
  <<immutable>>
  logical_access_name
  role_name
  access_type
  subunit
}

class BaseHistorico {
  <<immutable>>
  sid
  app_access_name
  role_name
  process_access   // REQUEST|GRANT|REVOKE
  record_date
  area
  subunit
}

class HeadCount {
  <<immutable>>
  sid
  mail
}

class Role {
  role_id
  app_name
  role_name
  access_type
}

class Person {
  sid
  area
  subunit
  updated_at
}

class PolicySubunitRole {
  subunit
  role_id
  -- PK (subunit, role_id)
}

class vw_current_assignments {
  <<view>>
  sid
  role_key   // app_name::role_name
}

class vw_should_assignments {
  <<view>>
  sid
  role_key
}

class vw_to_grant {
  <<view>>
  sid
  role_key
}

class vw_to_revoke {
  <<view>>
  sid
  role_key
}

class vw_access_report {
  <<view>>
  sid
  role_key
  estado   // TIENE | DEBE | DAR | QUITAR
  fuente   // CURRENT | SHOULD | DIFF
}

BaseApplication --> Role : "normalización mínima"
BaseHistorico --> Person : "último subunit por SID"
HeadCount --> Person : "SID→mail"

Person --> PolicySubunitRole : "subunit"
Role --> PolicySubunitRole : "rol permitido"

BaseHistorico --> vw_current_assignments : "último GRANT/REVOKE"
Person --> vw_should_assignments
PolicySubunitRole --> vw_should_assignments
Role --> vw_should_assignments

vw_should_assignments --> vw_to_grant : "diff"
vw_current_assignments --> vw_to_grant

vw_current_assignments --> vw_to_revoke : "diff"
vw_should_assignments --> vw_to_revoke

vw_current_assignments --> vw_access_report
vw_should_assignments --> vw_access_report
vw_to_grant --> vw_access_report
vw_to_revoke --> vw_access_report
--------------------------------------------------------------------


erDiagram
  %% ========= BASES (no editables) =========
  BaseApplication {
    string logical_access_name
    string role_name
    string access_type
    string subunit
    %% ...otros campos de catálogo
  }

  BaseHistorico {
    string sid
    string app_access_name
    string role_name
    string process_access  "REQUEST|GRANT|REVOKE"
    date   record_date
    string area
    string subunit
    %% ...otros campos del histórico
  }

  HeadCount {
    string sid PK  
    string mail
  }

  %% ========= TABLAS OPERATIVAS (mínimas) =========
  Role {
    uuid   role_id PK
    string app_name
    string role_name
    string access_type
  }

  Person {
    string sid PK
    string area
    string subunit
    timestamp updated_at
  }

  PolicySubunitRole {
    string subunit
    uuid   role_id FK
    %% PK (subunit, role_id)
  }

  %% ========= VISTAS DE SALIDA (lo que pediste) =========
  vw_current_assignments {
    %% <<view>>  TIENE
    string sid
    string role_key  "app_name::role_name"
  }

  vw_should_assignments {
    %% <<view>>  DEBE
    string sid
    string role_key  "app_name::role_name"
  }

  vw_to_grant {
    %% <<view>>  DAR = SHOULD - HAS
    string sid
    string role_key
  }

  vw_to_revoke {
    %% <<view>>  QUITAR = HAS - SHOULD
    string sid
    string role_key
  }

  vw_access_report {
    %% <<view>>  RESUMEN ÚNICO
    string sid
    string role_key
    string estado  "TIENE|DEBE|DAR|QUITAR"
    string fuente  "CURRENT|SHOULD|DIFF"
  }

  %% ========= RELACIONES (con etiquetas) =========
  BaseApplication ||--o{ Role : "normaliza roles"
  BaseHistorico  ||--o{ Person : "último subunit por SID"
  HeadCount ||--|| Person : "join por SID (obtener mail)"

  Person ||--o{ PolicySubunitRole : "join por subunit"
  Role   ||--o{ PolicySubunitRole : "roles permitidos"

  BaseHistorico ||--o{ vw_current_assignments : "último GRANT/REVOKE"
  Person ||--o{ vw_should_assignments : "subunit→roles"
  PolicySubunitRole ||--o{ vw_should_assignments : ""
  Role ||--o{ vw_should_assignments : "formar role_key"

  vw_should_assignments }o--o{ vw_to_grant : "diff SHOULD - HAS"
  vw_current_assignments }o--o{ vw_to_grant : ""

  vw_current_assignments }o--o{ vw_to_revoke : "diff HAS - SHOULD"
  vw_should_assignments }o--o{ vw_to_revoke : ""

  vw_current_assignments }o--o{ vw_access_report : "UNION TIENE"
  vw_should_assignments }o--o{ vw_access_report : "UNION DEBE"
  vw_to_grant }o--o{ vw_access_report : "UNION DAR"
  vw_to_revoke }o--o{ vw_access_report : "UNION QUITAR"
