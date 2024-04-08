
#~ Khai báo các thư viện cần thiết
from sklearn.tree import DecisionTreeClassifier
import random
import numpy as np
import os

#~ Đường dẫn đến file wordlist.txt
file_path = os.path.join(os.path.dirname(__file__), 'wordlist.txt')

#~ Đọc nội dung từ file
with open(file_path, 'r') as file:
    word_list = [line.strip() for line in file]
    
#? Dòng này mở file wordlist.txt và đọc từng dòng. Sau đó, nội dung từng dòng
#? được lưu vào danh sách word_list sau khi xóa khoảng trắng và ký tự xuống dòng.

#~ Tạo dữ liệu huấn luyện tự động
training_data = [{'word': word, 'label': index} for index, word in enumerate(word_list)]

#? Dòng này tạo một danh sách từ điển training_data, trong đó mỗi từ điển đại diện
#? cho một từ trong word_list và chứa hai khóa là 'word' và 'label'. 'word' lưu trữ từ
#? và 'label' lưu trữ chỉ mục tương ứng của từ trong word_list.
#// print(training_data)

#~ Chuẩn bị dữ liệu huấn luyện
def get_encoded_word(word):
    encoded_word = [ord(char) - ord('a') for char in word]
    return encoded_word

#? Dòng này định nghĩa hàm để chuyển đổi từ thành một danh sách gồm các số nguyên,
#? biểu diễn các ký tự của từ theo thứ tự từ "a" đến "z".

#~ Tìm độ dài tối đa của các từ
max_length = max(len(data['word']) for data in training_data)

#? Tìm độ dài lớn nhất của các từ trong training_data.

#~ Pad các sequence về cùng độ dài tối đa
X_train = np.array([get_encoded_word(data['word']) + [0] * (max_length - len(data['word'])) for data in training_data])
#// print(X_train)

#? Tạo một mảng NumPy X_train với kích thước (số lượng từ, độ dài lớn nhất)
#? Mỗi từ trong training_data được chuyển đổi thành danh sách các số nguyên bằng cách sử dụng get_encoded_word(word)
#? Sau đó, dữ liệu được thêm các số 0 vào cuối để đảm bảo cùng độ dài với max_length

y_train = np.array([data['label'] for data in training_data])
#? Tạo một mảng NumPy y_train chứa chỉ mục tương ứng của từ trong word_list

#~ Tạo một đối tượng DecisionTreeClassifier và huấn luyện cây quyết định
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

#~ Hàm để lấy dự đoán từ cây quyết định
def get_decision_tree_prediction(guessed_word):
    encoded_word = get_encoded_word(guessed_word)
    padded_word = encoded_word + [0] * (max_length - len(encoded_word))
    prediction = clf.predict([padded_word])

    #~ Kiểm tra nếu dự đoán là ký tự chữ cái
    if prediction[0] >= 0 and prediction[0] <= 25:
        return chr(prediction[0] + ord('a'))
    else:
        return None
#? chuyển đổi từ thành danh sách các số nguyên bằng get_encoded_word(guessed_word)
#? Sau đó, nó thêm các số 0 vào cuối danh sách để có cùng độ dài max_length.
#? Cuối cùng, nó sử dụng cây quyết định đã huấn luyện để dự đoán và trả về ký tự được dự đoán.

#~ Hàm để chơi trò chơi
def play_game():
    #~ Nhập số lượng ký tự từ người chơi
    while True:
        word_length = input("Nhập số lượng ký tự: ")
        if word_length.isdigit():
            word_length = int(word_length)
            candidate_words = [word for word in word_list if len(word) == word_length]
            if not candidate_words:
                print(f"Không tìm thấy từ nào có độ dài {word_length}. Vui lòng thử lại.")
                continue
            target_word = random.choice(candidate_words).lower()
            break
        else:
            print("Vui lòng nhập một số nguyên dương.")
    #~ Đặt giới hạn số lượt đoán
    max_wrong_guesses = 10

    #~ Khởi tạo từ ban đầu
    guessed_word = ['_'] * word_length
    wrong_guesses = set()

    #~ Bắt đầu trò chơi
    while True:
        print("="*40)
        #~ print(f"Lượt đoán thứ {num_guesses+1}:")
        print("* Từ đang được đoán:", ' '.join(guessed_word))
        guess = input("* Đoán một ký tự: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Vui lòng nhập một ký tự chữ cái.")
            continue

        if guess in guessed_word or guess in wrong_guesses:
            print("Bạn đã đoán ký tự này rồi.")
            continue

        #~ Kiểm tra đoán đúng
        if guess in target_word:
            indices = [i for i, char in enumerate(target_word) if char == guess]
            for index in indices:
                guessed_word[index] = guess
            print('='*40)
            print("* Ký tự đoán đúng!")
            print("* Từ đang được đoán:", ' '.join(guessed_word))
        else:
            print('='*40)
            print("* Từ đang được đoán:", ' '.join(guessed_word))
            print("* Ký tự đoán sai.")
            wrong_guesses.add(guess)
            print("* Các ký tự đã đoán sai:", ' '.join(wrong_guesses))
            print(f"Số lần đoán sai còn lại: {max_wrong_guesses - len(wrong_guesses)}")
            #~ wrong_guesses.append(guess)
        

        #~ Kiểm tra xem đã đoán đúng toàn bộ từ chưa
        if '_' not in guessed_word:
            print('='*40)
            print("* Chúc mừng! Bạn đã đoán đúng từ.")
            break
        
        elif len(wrong_guesses) == max_wrong_guesses:
            print("Bạn đã đạt đến giới hạn số lượng ký tự sai.")
            print(f"Từ cần đoán là: {target_word}")
            break

        #~ Đưa ra dự đoán từ cây quyết định
        if '_' in guessed_word:
            next_index = guessed_word.index('_')
            prediction = get_decision_tree_prediction(''.join(guessed_word))
            if prediction is None:
                print("Máy không thể đoán tiếp.")
            elif prediction not in candidate_words:
                print("Dự đoán của máy không hợp lệ.")
            else:
                print("Dự đoán ký tự tiếp theo của máy:", prediction)
                guessed_word[next_index] = prediction                
    print('='*40)
    print('--> Kết thúc! Từ cần đoán là:', target_word)


#~ Chạy trò chơi
play_game()
