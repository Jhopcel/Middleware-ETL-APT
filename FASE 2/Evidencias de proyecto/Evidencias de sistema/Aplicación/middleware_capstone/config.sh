#!/bin/bash
DIRECT="$PWD"
LOCAL_METADATA_AIRFLOW=$(grep '^LOCAL_CONNECTION_TO_METADATA_DB=' .env | xargs | sed 's/^LOCAL_CONNECTION_TO_METADATA_DB=//' | tr -d '[:space:]')
# Imprimir el directorio actual
echo "Tu ruta de directorio actual = $DIRECT"
export AIRFLOW_HOME=$DIRECT
export AIRFLOW__CORE__DAGS_FOLDER=$DIRECT/workflows/dags
export AIRFLOW__CORE__PLUGINS_FOLDER=$DIRECT/plugins
export AIRFLOW__LOGGING__BASE_LOG_FOLDER=$DIRECT/logs
export AIRFLOW__LOGGING__DAG_PROCESSOR_MANAGER_LOG_LOCATION=$DIRECT/logs/dag_processor_manager/dag_processor_manager.log
export AIRFLOW__WEBSERVER__CONFIG_FILE=$DIRECT/webserver_config.py
export AIRFLOW__SCHEDULER__CHILD_PROCESS_LOG_DIRECTORY=$DIRECT/logs/scheduler

load_local_db() {
    export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:///$DIRECT/airflow.db
    echo $AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
}

if [ "$LOCAL_METADATA_AIRFLOW" == "" ]; then
    echo "Parece que no cuentas con una conexión ¿Deseas cargar la base de datos de forma local?"
    echo "1 - Sí"
    echo "2 - No"
    read -p "Selecciona una opción: " option
    case $option in
        1)
            load_local_db
            ;;
        2)
            echo "No se cargará la base de datos"
            ;;
        *)
            echo "Opción no válida"
            ;;
    esac
else
    load_local_db
fi