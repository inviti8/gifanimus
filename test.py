from gifanimus import GifAnimation
import time

loading = GifAnimation('./loading.gif', 1000, True, 'LOADING...')

time.sleep(3)

loading.Play()

time.sleep(10)

loading.Stop()
