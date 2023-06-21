from __future__ import annotations

from trees import UniqueBinaryTree


def main():
    tree = UniqueBinaryTree()
    tree.append(10)
    tree.append(5)
    tree.append(110)
    
    tree.display(method='inorder')


if __name__ == '__main__':
    main()