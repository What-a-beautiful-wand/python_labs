from collections import deque

def stack_is_empty(st) -> bool:
    return (not st)

def stack_push(st: list, item: Any) -> None:
    st.append(item)
    return None

def stack_pop(st) -> Any:
    if stack_is_empty(st):
        raise IndexError("Пустой стек")
    return st.pop()

#=============================================================

def queue_enqueue(q, item) -> None:
    q.append(item)
    return None

def queue_dequeue(q) -> Any:
    return q.popleft()

def queue_peek(q) -> Any | None: