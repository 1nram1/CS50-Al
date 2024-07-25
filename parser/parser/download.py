from nltk import Tree

# 构建句子的句法树
tree = Tree('S', [
    Tree('NP', [
        Tree('DT', ['The']),
        Tree('NN', ['book']),
        Tree('SBAR', [
            Tree('WHNP', ['that']),
            Tree('S', [
                Tree('NP', ['Alice']),
                Tree('VP', [
                    Tree('VBD', ['wrote'])
                ])
            ])
        ])
    ]),
    Tree('VP', [
        Tree('VBD', ['was']),
        Tree('PP', [
            Tree('IN', ['on']),
            Tree('NP', [
                Tree('DT', ['the']),
                Tree('NN', ['table'])
            ])
        ])
    ])
])

# 打印树结构
print(tree)

# 可视化树结构
tree.draw()

