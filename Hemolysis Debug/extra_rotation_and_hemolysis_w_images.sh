/file/read-case-data "C5_SBES_19M_T-1-24000.cas.h5"


/solve/execute-commands/add-edit proc-stats 4 "time-step" "/report/system/proc-stats"
/solve/execute-commands/add-edit partition-info 4 "time-step" "/parallel/partition/print-active-partitions"
/solve/execute-commands/add-edit usage-stats 4 "time-step" "/parallel/timer/usage"
/solve/execute-commands/add-edit usage-reset 4 "time-step" "/parallel/timer/reset"
/solve/execute-commands/add-edit bandwidth 4 "time-step" "/parallel/bandwidth"

/solve/dual-time-iterate 1600 120;[max timesteps, iterations per step]
