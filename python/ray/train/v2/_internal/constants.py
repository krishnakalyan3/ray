import os
from typing import Dict

from ray._private.ray_constants import env_bool, env_set_by_user

# Unsupported configs can use this value to detect if the user has set it.
_UNSUPPORTED = "UNSUPPORTED"
_DEPRECATED = "DEPRECATED"

# The name of the file that is used to validate the storage.
VALIDATE_STORAGE_MARKER_FILENAME = ".validate_storage_marker"
# The name of the file that is used to store the checkpoint manager snapshot.
CHECKPOINT_MANAGER_SNAPSHOT_FILENAME = "checkpoint_manager_snapshot.json"


# -----------------------------------------------------------------------
# Environment variables used in the controller, workers, and state actor.
#
# Be sure to update ENV_VARS_TO_PROPAGATE when adding new
# environment variables in this section.
# -----------------------------------------------------------------------

# Polling interval for the Train controller.
# This determines how many seconds the controller will wait between
# polling the worker group for its status.
HEALTH_CHECK_INTERVAL_S_ENV_VAR = "RAY_TRAIN_HEALTH_CHECK_INTERVAL_S"
DEFAULT_HEALTH_CHECK_INTERVAL_S: float = 2.0

# The time in seconds a worker health check must be hanging for
# before the controller marks the worker as dead and handles the failure.
WORKER_HEALTH_CHECK_TIMEOUT_S_ENV_VAR = "RAY_TRAIN_WORKER_HEALTH_CHECK_TIMEOUT_S"
DEFAULT_WORKER_HEALTH_CHECK_TIMEOUT_S: float = 10 * 60

# Timeout in seconds for the worker group to start.
WORKER_GROUP_START_TIMEOUT_S_ENV_VAR = "RAY_TRAIN_WORKER_GROUP_START_TIMEOUT_S"
DEFAULT_WORKER_GROUP_START_TIMEOUT_S: float = 30.0

# Timeout in seconds for `ray.train.report` to block on synchronization barriers,
# after which a timeout error will be raised.
REPORT_BARRIER_TIMEOUT_S_ENV_VAR = "RAY_TRAIN_REPORT_BARRIER_TIMEOUT_S"
DEFAULT_REPORT_BARRIER_TIMEOUT_S: float = 60 * 30
# Time in seconds for `ray.train.report` to log a warning if it is waiting for sync
# actor notification of releasing.
REPORT_BARRIER_WARN_INTERVAL_S_ENV_VAR = "RAY_TRAIN_REPORT_BARRIER_WARN_INTERVAL_S"
DEFAULT_REPORT_BARRIER_WARN_INTERVAL_S: float = 60

# Environment variable to enable the print function patching.
ENABLE_PRINT_PATCH_ENV_VAR = "RAY_TRAIN_ENABLE_PRINT_PATCH"
DEFAULT_ENABLE_PRINT_PATCH = "1"

# V2 feature flag.
V2_ENABLED_ENV_VAR = "RAY_TRAIN_V2_ENABLED"

# Environment variables to enable/disable controller/worker structured logging.
ENABLE_CONTROLLER_STRUCTURED_LOGGING_ENV_VAR = (
    "RAY_TRAIN_ENABLE_CONTROLLER_STRUCTURED_LOGGING"
)
ENABLE_WORKER_STRUCTURED_LOGGING_ENV_VAR = "RAY_TRAIN_ENABLE_WORKER_STRUCTURED_LOGGING"
DEFAULT_ENABLE_CONTROLLER_LOGGING = "1"
DEFAULT_ENABLE_WORKER_LOGGING = "1"

# Environment variables to configure reconciliation interval for Train state actor.
# This determines how many seconds the state actor will wait between
# polling the controller for its status.
ENABLE_STATE_ACTOR_RECONCILIATION_ENV_VAR = (
    "RAY_TRAIN_ENABLE_STATE_ACTOR_RECONCILIATION"
)
DEFAULT_ENABLE_STATE_ACTOR_RECONCILIATION = "1"
STATE_ACTOR_RECONCILIATION_INTERVAL_S_ENV_VAR = (
    "RAY_TRAIN_STATE_ACTOR_RECONCILIATION_INTERVAL_S"
)
DEFAULT_STATE_ACTOR_RECONCILIATION_INTERVAL_S: float = 30.0
# TODO: `ray.util.state.api.get_actor` takes 10-50ms but we cannot pick lower than 2s
# due to https://github.com/ray-project/ray/issues/54153. Lower this after fix.
GET_ACTOR_TIMEOUT_S: int = 2
# GET_ACTOR_TIMEOUT_S_ENV_VAR * CONTROLLERS_TO_POLL_PER_ITERATION_ENV_VAR should be
# way less than STATE_ACTOR_RECONCILIATION_INTERVAL_S_ENV_VAR.
CONTROLLERS_TO_POLL_PER_ITERATION: int = 5
# Environment variable for Train execution callbacks
RAY_TRAIN_CALLBACKS_ENV_VAR = "RAY_TRAIN_CALLBACKS"

# Environment variables to propagate from the driver to the controller,
# and then from the controller to the workers.
ENV_VARS_TO_PROPAGATE = {
    V2_ENABLED_ENV_VAR,
    HEALTH_CHECK_INTERVAL_S_ENV_VAR,
    WORKER_HEALTH_CHECK_TIMEOUT_S_ENV_VAR,
    WORKER_GROUP_START_TIMEOUT_S_ENV_VAR,
    REPORT_BARRIER_TIMEOUT_S_ENV_VAR,
    REPORT_BARRIER_WARN_INTERVAL_S_ENV_VAR,
    ENABLE_PRINT_PATCH_ENV_VAR,
    ENABLE_CONTROLLER_STRUCTURED_LOGGING_ENV_VAR,
    ENABLE_WORKER_STRUCTURED_LOGGING_ENV_VAR,
    ENABLE_STATE_ACTOR_RECONCILIATION_ENV_VAR,
    STATE_ACTOR_RECONCILIATION_INTERVAL_S_ENV_VAR,
}


# ------------------------------------------------------------
# Environment variables used in the driver script only.
# ------------------------------------------------------------

# The environment variable to enable the Ray Train Metrics.
METRICS_ENABLED_ENV_VAR = "RAY_TRAIN_METRICS_ENABLED"

# Whether or not to run the controller as an actor.
RUN_CONTROLLER_AS_ACTOR_ENV_VAR = "RAY_TRAIN_RUN_CONTROLLER_AS_ACTOR"
DEFAULT_RUN_CONTROLLER_AS_ACTOR = "1"


def is_v2_enabled() -> bool:
    return env_bool(V2_ENABLED_ENV_VAR, False)


def get_env_vars_to_propagate() -> Dict[str, str]:
    """Returns a dictionary of environment variables that should be propagated
    from the driver to the controller, and then from the controller
    to each training worker.

    This way, users only need to set environment variables in one place
    when launching the script instead of needing to manually set a runtime environment.
    """
    env_vars = {}
    for env_var in ENV_VARS_TO_PROPAGATE:
        if env_set_by_user(env_var):
            env_vars[env_var] = os.environ[env_var]
    return env_vars
