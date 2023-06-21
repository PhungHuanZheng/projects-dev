from __future__ import annotations

from trees import UniqueBinaryTree


def main():
    tree = UniqueBinaryTree()
    for i in range(10):
        tree.append(10)

    print(tree.contains(10))
    
    tree.display(method='preorder')


if __name__ == '__main__':
    main()