from dataclasses import dataclass


@dataclass(frozen=True)
class UrlPatterns:
    root_url: str = "/"
    all_tasks: str = "/all_tasks"
    create_task: str = "/create-task"
    get_specific_task: str = "/tasks/{task_id}"
    update_specific_task: str = "/tasks/{task_id}/update"
    delete_specific_task: str = "/tasks/{task_id}/delete"
    tasks_set: str = "/tasks-set"
    get_common_title_tasks: str = "/tasks-by-title/{title}"
    get_common_description_tasks: str = "/tasks-by-description/{description}"
    get_all_done_or_undone_tasks: str = "/tasks-by-status/{is_done}"
