# ================================================================
# MUSIC STREAMING PLAYLIST MANAGER
# Data Structures: LinkedList, CircularLinkedList, Stack
# ================================================================

import random

# ----------------------------------------------------------------
# Song: lưu thông tin 1 bài hát
# ----------------------------------------------------------------
class Song:
    def __init__(self, song_id, title, artist, duration):
        self.song_id = song_id
        self.title   = title
        self.artist  = artist
        self.duration = int(duration)

    def __str__(self):
        mins = self.duration // 60
        secs = self.duration % 60
        return f"[{self.song_id}] {self.title} - {self.artist} ({mins}:{secs:02d})"

    def to_line(self):
        return f"{self.song_id}|{self.title}|{self.artist}|{self.duration}"


# ----------------------------------------------------------------
# Node: 1 ô trong danh sách liên kết
# ----------------------------------------------------------------
class Node:
    def __init__(self, song):
        self.song = song
        self.next = None


# ================================================================
# LinkedList: dùng cho Library và Favorites
# ================================================================
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def add(self, song):
        new_node = Node(song)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def remove_by_id(self, song_id):
        if not self.head:
            return False

        # Xóa node đầu tiên
        if self.head.song.song_id == song_id:
            if self.head == self.tail:
                self.tail = None
            self.head = self.head.next
            self.size -= 1
            return True

        # Xóa node ở giữa hoặc cuối
        current = self.head
        while current.next:
            if current.next.song.song_id == song_id:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def remove_by_title(self, title):
        if not self.head:
            return False

        title_lower = title.lower()

        # Xóa node đầu tiên
        if self.head.song.title.lower() == title_lower:
            if self.head == self.tail:
                self.tail = None
            self.head = self.head.next
            self.size -= 1
            return True

        # Xóa node ở giữa hoặc cuối
        current = self.head
        while current.next:
            if current.next.song.title.lower() == title_lower:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def display(self, label="List"):
        print(f"\n___{label}___")
        if not self.head:
            print("Music library is empty!")
            return
        current = self.head
        i = 1
        while current:
            print(f"{i}. {current.song}")
            current = current.next
            i += 1
        print("=" * 30)


# ================================================================
# CircularLinkedList: dùng cho Playlist (vòng lặp)
# ================================================================
class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def add(self, song):
        new_node = Node(song)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head       # 1 node tự trỏ về chính nó
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head       # tail luôn trỏ về head
        self.size += 1

    def remove_by_id(self, song_id):
        if self.is_empty():
            return False

        current = self.head
        prev    = self.tail   # node trước current (ban đầu là tail)

        for _ in range(self.size):
            if current.song.song_id == song_id:
                if self.size == 1:           # chỉ còn 1 node
                    self.head = None
                    self.tail = None
                elif current == self.head:   # xóa node đầu
                    self.head = current.next
                    self.tail.next = self.head
                elif current == self.tail:   # xóa node cuối
                    self.tail = prev
                    self.tail.next = self.head
                else:                        # xóa node giữa
                    prev.next = current.next
                self.size -= 1
                return True
            prev    = current
            current = current.next
        return False

    def remove_by_title(self, title):
        if self.is_empty():
            return False

        title_lower = title.lower()
        current = self.head
        prev    = self.tail

        for _ in range(self.size):
            if current.song.title.lower() == title_lower:
                if self.size == 1:
                    self.head = None
                    self.tail = None
                elif current == self.head:
                    self.head = current.next
                    self.tail.next = self.head
                elif current == self.tail:
                    self.tail = prev
                    self.tail.next = self.head
                else:
                    prev.next = current.next
                self.size -= 1
                return True
            prev    = current
            current = current.next
        return False

    def display(self):
        print("\n___PLAYLIST___")
        if self.is_empty():
            print("Playlist is empty!")
            return
        current = self.head
        for i in range(1, self.size + 1):
            print(f"{i}. {current.song}")
            current = current.next
        print("=" * 30)

    def shuffle(self):
        if self.size < 2:
            print("Need at least 2 songs in playlist to shuffle!")
            return

        # Lấy tất cả bài ra list bình thường
        songs = []
        current = self.head
        for _ in range(self.size):
            songs.append(current.song)
            current = current.next

        # Xáo trộn bằng Fisher-Yates
        for i in range(len(songs) - 1, 0, -1):
            j = random.randint(0, i)
            songs[i], songs[j] = songs[j], songs[i]

        # Xây lại Circular Linked List từ list đã xáo
        self.head = None
        self.tail = None
        self.size = 0
        for song in songs:
            self.add(song)

        print("Playlist shuffled!")


# ================================================================
# Stack: dùng cho Recently Played (LIFO - bài mới nhất ở trên)
# ================================================================
class Stack:
    def __init__(self):
        self.top  = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def push(self, song):
        new_node      = Node(song)
        new_node.next = self.top
        self.top      = new_node
        self.size     += 1

    def pop(self):
        if self.top is None:
            return None
        removed  = self.top
        self.top = self.top.next
        self.size -= 1
        return removed.song

    def display(self):
        print("\n___RECENTLY PLAYED___")
        if self.is_empty():
            print("No songs played yet!")
            return
        current = self.top
        i = 1
        while current:
            print(f"{i}. {current.song}")
            current = current.next
            i += 1
        print("=" * 30)


# ================================================================
# MusicPlayer: điều khiển toàn bộ chương trình
# ================================================================
class MusicPlayer:
    def __init__(self):
        self.library        = LinkedList()
        self.favorites      = LinkedList()
        self.playlist       = CircularLinkedList()
        self.recently_played = Stack()
        self.current_song   = None     # bài đang phát
        self.now_playing_node = None   # node đang phát trong playlist

    # ── FILE ────────────────────────────────────────────────────

    def load_from_file(self, filename="songs.txt"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('|')
                        if len(parts) == 4:
                            song = Song(parts[0], parts[1], parts[2], parts[3])
                            self.library.add(song)
            print(f"Loaded '{filename}' successfully!")
        except FileNotFoundError:
            print(f"File '{filename}' not found. Starting with empty library.")

    def save_to_file(self, filename="songs.txt"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                current = self.library.head
                while current:
                    f.write(current.song.to_line() + "\n")
                    current = current.next
            print("Data saved successfully!")
        except Exception:
            print("Error: Could not save file.")

    # ── LIBRARY ─────────────────────────────────────────────────

    def add_to_playlist(self):
        self.library.display("MUSIC LIBRARY")
        song_id = input("Enter Song ID to add to Playlist: ").strip()
        current = self.library.head
        while current:
            if current.song.song_id == song_id:
                self.playlist.add(current.song)
                print(f"Added '{current.song.title}' to Playlist!")
                return
            current = current.next
        print("Song not found in Library!")
    
    def add_to_favorites(self):
        self.library.display("MUSIC LIBRARY")
        song_id = input("Enter Song ID to add to Favorites: ").strip()

        current = self.library.head

        while current:
            if current.song.song_id == song_id:
                self.favorites.add(current.song)
                print(f"Added '{current.song.title}' to Favorites!")
                return
            current = current.next

        print("Song not found in Library!")

    def play_favorites(self):

        if self.favorites.is_empty():
            print("Favorites is empty!")
            return

        current = self.favorites.head

        print("\nPLAYING FAVORITES")

        while current:
            print(f"Now Playing: {current.song}")
            self.recently_played.push(current.song)

            input("Press Enter for next song...")

            current = current.next
    

    # ── PLAYLIST ────────────────────────────────────────────────

    def play_next(self):
        """Phát bài tiếp theo. Playlist vòng lặp nên sau bài cuối sẽ quay về bài đầu."""
        if self.playlist.is_empty():
            print("Playlist is empty! Add songs first.")
            return

        if self.now_playing_node is None:
            # Chưa phát bài nào -> bắt đầu từ đầu playlist
            self.now_playing_node = self.playlist.head
        else:
            # .next tự động vòng lại đầu nhờ Circular Linked List
            self.now_playing_node = self.now_playing_node.next

        self.current_song = self.now_playing_node.song
        self.recently_played.push(self.current_song)
        print(f"\nNow Playing: {self.current_song}")

    def play_previous(self):
        """Phát bài trước đó. Duyệt vòng để tìm node đứng trước node hiện tại."""
        if self.playlist.is_empty():
            print("Playlist is empty! Add songs first.")
            return

        if self.now_playing_node is None:
            # Chưa phát bài nào -> bắt đầu từ bài cuối (tail)
            self.now_playing_node = self.playlist.tail
        else:
            # Tìm node đứng ngay TRƯỚC now_playing_node trong vòng tròn
            prev_node = self.playlist.head
            for _ in range(self.playlist.size):
                if prev_node.next == self.now_playing_node:
                    break
                prev_node = prev_node.next
            self.now_playing_node = prev_node

        self.current_song = self.now_playing_node.song
        self.recently_played.push(self.current_song)
        print(f"\nNow Playing (Previous): {self.current_song}")

    def shuffle_playlist(self):
        self.playlist.shuffle()
        self.now_playing_node = None   # reset vì thứ tự đã thay đổi
        self.playlist.display()

    # ── REMOVE ──────────────────────────────────────────────────

    def remove_song(self):
        print("\nRemove from which list?")
        print("1. Library")
        print("2. Playlist")
        print("3. Favorites")
        loc      = input("Choose: ").strip()
        key_type = input("Remove by (1: ID  /  2: Title): ").strip()
        value    = input("Enter value: ").strip()

        if loc == '1':
            list_name     = "Library"
            remove_by_id    = self.library.remove_by_id
            remove_by_title = self.library.remove_by_title
        elif loc == '2':
            list_name     = "Playlist"
            remove_by_id    = self.playlist.remove_by_id
            remove_by_title = self.playlist.remove_by_title
        elif loc == '3':
            list_name     = "Favorites"
            remove_by_id    = self.favorites.remove_by_id
            remove_by_title = self.favorites.remove_by_title
        else:
            print("Invalid choice!")
            return

        if key_type == '1':
            success = remove_by_id(value)
        else:
            success = remove_by_title(value)

        if success:
            # Nếu xóa bài đang phát khỏi playlist -> reset con trỏ
            if loc == '2' and self.now_playing_node is not None:
                if key_type == '1':
                    removed_current = (self.now_playing_node.song.song_id == value)
                else:
                    removed_current = (self.now_playing_node.song.title.lower() == value.lower())
                if removed_current:
                    self.now_playing_node = None
            print(f"Song removed from {list_name} successfully!")
        else:
            print(f"Song not found in {list_name}!")

    # ── MENU ────────────────────────────────────────────────────

    def menu(self):
        self.load_from_file()

        while True:
            print("\n" + "=" * 60)
            print("          MUSIC STREAMING PLAYLIST MANAGER")
            print("=" * 60)

            print("  --- LIBRARY ---")
            print("  1.  View Library")
            print("  2.  Add Song to Playlist")
            print("  3.  Add Song to Favorites")

            print("  --- PLAYLIST ---")
            print("  4.  View Playlist")
            print("  5.  Play Next Song")
            print("  6.  Play Previous Song")
            print("  7.  Shuffle Playlist")

            print("  --- RECENTLY PLAYED ---")
            print("  8.  View Recently Played")

            print("  --- FAVORITES ---")
            print("  9.  View Favorites")
            print("  10.  Play Favorites")

            print("  --- MANAGE ---")
            print("  11. Remove a Song")
            print("  12. Save Data")

            print("  0.  Exit")
            print("=" * 60)

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.library.display("MUSIC LIBRARY")
            elif choice == '2':
                self.add_to_playlist()
            elif choice == '3':
                self.add_to_favorites()
            elif choice == '4':
                self.playlist.display()
            elif choice == '5':
                self.play_next()
            elif choice == '6':
                self.play_previous()
            elif choice == '7':
                self.shuffle_playlist()
            elif choice == '8':
                self.recently_played.display()
            elif choice == '9':
                self.favorites.display("FAVORITES")
            elif choice == '10':
                self.play_favorites()
            elif choice == '11':
                self.remove_song()
            elif choice == '12':
                self.save_to_file()
            elif choice == '0':
                self.save_to_file()
                print("Goodbye! See you next time!")
                break
            else:
                print("Invalid choice! Please enter 0-11.")


# ====================== RUN ======================
if __name__ == "__main__":
    player = MusicPlayer()
    player.menu()
