from torrentp import TorrentDownloader
tor=input()
torrent_file = TorrentDownloader(tor, '.')
torrent_file.start_download()
