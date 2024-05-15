def main():
    # Foydalanuvchidan ikkita butun son kiritilishi so'raladi
    birinchi_raqam = int(input("Birinchi raqamni kiriting: "))
    ikkinchi_raqam = int(input("Ikkinchi raqamni kiriting: "))

    # Operatorlarni ro'yxat qilib olamiz
    operatorlar = ['+', '-', '*', '/']

    # Operatorlardan birini so'ramiz va foydalanuvchining kiritgan operator bilan taqqoslaymiz
    amal = input("Amalni kiriting (+, -, *, /): ")
    while amal not in operatorlar:
        print("Noto'g'ri amal kiritildi. Qaytadan urinib ko'ring.")
        amal = input("Amalni kiriting (+, -, *, /): ")

    # Natijani hisoblash
    if amal == '+':
        natija = birinchi_raqam + ikkinchi_raqam
    elif amal == '-':
        natija = birinchi_raqam - ikkinchi_raqam
    elif amal == '*':
        natija = birinchi_raqam * ikkinchi_raqam
    elif amal == '/':
        natija = birinchi_raqam / ikkinchi_raqam

    # Foydalanuvchining javobini so'raladi
    foydalanuvchi_javobi = float(input("Sizcha, {} va {} ni {} amalining natijasi qanday bo'lishi kerak? ".format(birinchi_raqam, ikkinchi_raqam, amal)))

    # Foydalanuvchining kiritgan javobi to'g'ri yoki noto'g'ri ekanligini tekshirish
    if foydalanuvchi_javobi == natija:
        print("To'g'ri!")
    else:
        print("Noto'g'ri! To'g'ri javob: ", natija)

if __name__ == "__main__":
    main()
