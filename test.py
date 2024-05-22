from gifanimus import LoadingGif
import time

loading = LoadingGif('./loading.gif', 4000)

time.sleep(10)

loading.Stop()
