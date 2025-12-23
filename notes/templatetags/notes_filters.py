from django import template

register = template.Library()

@register.filter
def filter_priority(notes, priority):
    """过滤指定优先级的笔记"""
    if hasattr(notes, 'filter'):
        # 如果是QuerySet
        return notes.filter(priority=priority)
    else:
        # 如果是列表
        return [note for note in notes if note.priority == priority]

@register.filter
def filter_completed(notes, completed):
    """过滤完成状态的笔记"""
    completed_bool = completed in [True, 'True', 'true', '1', 1]
    if hasattr(notes, 'filter'):
        # 如果是QuerySet
        return notes.filter(is_completed=completed_bool)
    else:
        # 如果是列表
        return [note for note in notes if note.is_completed == completed_bool]