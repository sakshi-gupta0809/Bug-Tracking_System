# from menu import show_menu
# src/main.py
# from menu import show_menu

# if __name__ == "__main__":
#     show_menu()

from src.menu import show_menu  # ✅ Absolute import when running with `-m`

if __name__ == "__main__":
    show_menu()

