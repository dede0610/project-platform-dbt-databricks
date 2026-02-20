{% macro generate_schema_name(custom_schema_name, node) -%}

    {{ vg_dbt_utils.generate_schema_name(custom_schema_name, node) }}

{%- endmacro %}
