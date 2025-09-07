from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import numpy as np

class TicTacToe(TwoPlayerGame):
    def __init__(self, players):
        # Khởi tạo bảng 3x3 rỗng (0 = trống, 1 = X, 2 = O)
        self.board = np.zeros((3, 3), dtype=int)
        self.players = players
        self.current_player = 1  # Player 1 bắt đầu (X)
    
    def possible_moves(self):
        """Trả về danh sách các nước đi có thể (các ô trống)"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    moves.append((i, j))
        return moves
    
    def make_move(self, move):
        """Thực hiện nước đi"""
        i, j = move
        self.board[i][j] = self.current_player
    
    def unmake_move(self, move):
        """Hoàn tác nước đi (cần thiết cho thuật toán Minimax)"""
        i, j = move
        self.board[i][j] = 0
    
    def lose(self):
        """Kiểm tra xem người chơi hiện tại có thua không"""
        return self.check_winner() == (3 - self.current_player)
    
    def is_over(self):
        """Kiểm tra xem trò chơi đã kết thúc chưa"""
        return self.check_winner() != 0 or len(self.possible_moves()) == 0
    
    def check_winner(self):
        """
        Kiểm tra người thắng
        Trả về: 0 = chưa có winner, 1 = player 1 (X), 2 = player 2 (O)
        """
        # Kiểm tra hàng ngang
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]
        
        # Kiểm tra hàng dọc
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != 0:
                return self.board[0][j]
        
        # Kiểm tra đường chéo chính
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        
        # Kiểm tra đường chéo phụ
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]
        
        return 0
    
    def scoring(self):
        """
        Hàm đánh giá cho thuật toán Minimax
        Trả về điểm số từ góc nhìn của người chơi hiện tại
        """
        winner = self.check_winner()
        if winner == self.current_player:
            return 100  # Thắng
        elif winner == (3 - self.current_player):
            return -100  # Thua
        else:
            return 0  # Hòa hoặc chưa kết thúc
    
    def show(self):
        """Hiển thị bàn cờ"""
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        print("\n   0   1   2")
        print("  -----------")
        for i in range(3):
            row = f"{i} | "
            for j in range(3):
                row += f"{symbols[self.board[i][j]]} | "
            print(row)
            print("  -----------")
        print()


def get_human_move(game):
    """Lấy nước đi từ người chơi"""
    while True:
        try:
            move_str = input("Nhập nước đi của bạn (hàng,cột): ")
            i, j = map(int, move_str.split(','))
            if (i, j) in game.possible_moves():
                return (i, j)
            else:
                print("Nước đi không hợp lệ! Vui lòng chọn ô trống.")
        except:
            print("Format không đúng! Vui lòng nhập theo format 'hàng,cột' (ví dụ: 1,2)")


def play_game():
    """Hàm chính để chơi game"""
    print("=== TIC TAC TOE với Minimax Algorithm ===")
    print("Bạn là X, AI là O")
    print("Nhập tọa độ theo format 'hàng,cột' (0,2)")
    
    # Tạo AI player với thuật toán Negamax (tương đương Minimax với Alpha-Beta pruning)
    # Depth = 9 đảm bảo AI chơi hoàn hảo (vì Tic Tac Toe có tối đa 9 nước)
    ai_algo = Negamax(9)
    
    # Khởi tạo game với Human player và AI player
    game = TicTacToe([Human_Player(get_human_move), AI_Player(ai_algo)])
    
    # Bắt đầu game
    game.play()
    
    # Hiển thị kết quả
    winner = game.check_winner()
    if winner == 1:
        print("Chúc mừng! Bạn đã thắng!")
    elif winner == 2:
        print("AI thắng! Chúc bạn may mắn lần sau!")
    else:
        print("Trò chơi hòa!")


def demo_ai_vs_ai():
    """Demo AI vs AI để xem thuật toán hoạt động"""
    print("\n=== AI vs AI ===")
    print("Giả lập 2 AI đấu với nhau")
    
    # Tạo 2 AI với độ sâu khác nhau
    ai1 = AI_Player(Negamax(9))  # AI mạnh
    ai2 = AI_Player(Negamax(5))  # AI yếu hơn
    
    game = TicTacToe([ai1, ai2])
    game.play()
    
    winner = game.check_winner()
    if winner == 1:
        print("AI Player 1 (X) thắng!")
    elif winner == 2:
        print("AI Player 2 (O) thắng!")
    else:
        print("Trò chơi hòa!")


if __name__ == "__main__":
    # Menu lựa chọn
    while True:
        print("-------------------------------")
        print("Chọn chế độ chơi:")
        print("1. Chơi với AI")
        print("2. AI vs AI")
        print("3. Thoát")
        choice = input("Nhập lựa chọn (1, 2 hoặc 3): ")

        if choice == "1":
            play_game()
            break
        elif choice == "2":
            demo_ai_vs_ai()
            break
        elif choice == "3":
            print("Cảm ơn bạn đã chơi!")
            break
        else:
            print("Lựa chọn không hợp lệ!\n-------------------------------\n")