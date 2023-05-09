OWNER(g:videocrawl)

PY3_LIBRARY()

PY_SRCS(
    __init__.py
    base.py
    buffered.py
    dishonest.py
    file.py
    ydb.py
    yt.py
    buffers/base.py
    buffers/simple.py
)

PEERDIR(
    ydb/public/sdk/python
    yt/python/yt/wrapper
    yt/python/client
)

END()
