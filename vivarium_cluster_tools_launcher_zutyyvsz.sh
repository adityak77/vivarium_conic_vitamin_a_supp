
    export VIVARIUM_LOGGING_DIRECTORY=/share/costeffectiveness/results/nigeria/2019_08_06_13_13_56/logs/2019_08_06_13_13_56_run/worker_logs
    export PYTHONPATH=/ihme/costeffectiveness/results/nigeria/2019_08_06_13_13_56:$PYTHONPATH

    /ihme/homes/adityak7/miniconda3/envs/vivarium_2017/bin/rq worker -c settings --name ${JOB_ID}.${SGE_TASK_ID} --burst -w "vivarium_cluster_tools.psimulate.distributed_worker.ResilientWorker" --exception-handler "vivarium_cluster_tools.psimulate.distributed_worker.retry_handler" vivarium

    