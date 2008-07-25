import unittest
import doctest

from muppy import tree

class TreeTest(unittest.TestCase):

    def test_node(self):
        """Check node functionality.

        Nodes can be created, linked to each other, and the output function
        should return the expected result.

        """
        # default representation
        n = tree.Node(1)
        expected = str(1)
        self.assert_(str(n) == expected)
        # custom representation
        expected = 'the quick brown fox'
        def foo(o): return expected
        n = tree.Node(1, foo)
        self.assert_(str(n) == expected)
        # attach child
        n.children.append(2)
        
    def test_get_referrers_tree(self):
        #root <- ref1 <- ref11
        #     <- ref11 (already included)
        #     <- ref2 <- ref22
        root = 'root id'
        ref1 = [root]
        ref11 = [ref1, root]
        ref2 = {1: root}
        ref22 = {1: ref2}

        res = tree.get_referrers_tree(root)
        # note that ref11 should not be included due to the repeat argument
        refs = [ref1, ref2]
        children = [c.o for c in res.children if isinstance(c, tree.Node)]
        for r in refs:
            self.assert_(r in children)
        self.assert_(ref11 not in children)
        # now we test the repeat argument
        res = tree.get_referrers_tree(root, repeat=True)
        refs = [ref1, ref11, ref2]
        children = [c.o for c in res.children if isinstance(c, tree.Node)]
        for r in refs:
            self.assert_(r in children)
        # test if maxdepth is working
        res = tree.get_referrers_tree(root, maxdepth=0)
        self.assert_(len(res.children) == 0)
        res = tree.get_referrers_tree(root, maxdepth=1)
        for c in res.children:
            if c == ref1:
                self.assert_(len(c.children) == 0)
        # test if the str_func is applied correctly
        expected = 'the quick brown fox'
        def foo(o): return expected
        res = tree.get_referrers_tree(root, str_func=foo)
        self.assert_(str(res) == expected)
        res = tree.get_referrers_tree(root, str_func=foo, repeat=True)
        self.assert_(str(res) == expected)

test_print_tree = """
At first we need to set up a sample tree with three children, each having
five string leaves and some have references to other children

>>> root = tree.Node('root')
>>> branch1 = tree.Node('branch1')
>>> root.children.append(branch1)
>>> branch2 = tree.Node('branch2')
>>> root.children.append(branch2)
>>> branch3 = tree.Node('branch3')
>>> root.children.append(branch3)
>>> branch2.children.append(branch3)
>>> branch3.children.append(branch1)
>>> for i in ['a','b','c','d','e']:
...     branch1.children.append(i)
...     branch2.children.append(i)
...     branch3.children.append(i)

let's start with a small tree first

>>> tree.print_tree(root, 1)
root-+-branch1
     +-branch2
     +-branch3

okay, next level
>>> tree.print_tree(root, 2)
root-+-branch1-+-a
     |         +-b
     |         +-c
     |         +-d
     |         +-e
     |
     +-branch2-+-branch3
     |         +-a
     |         +-b
     |         +-c
     |         +-d
     |         +-e
     |
     +-branch3-+-branch1
               +-a
               +-b
               +-c
               +-d
               +-e

and now full size

>>> tree.print_tree(root)
root-+-branch1-+-a
     |         +-b
     |         +-c
     |         +-d
     |         +-e
     |
     +-branch2-+-branch3-+-branch1-+-a
     |         |         |         +-b
     |         |         |         +-c
     |         |         |         +-d
     |         |         |         +-e
     |         |         |
     |         |         +-a
     |         |         +-b
     |         |         +-c
     |         |         +-d
     |         |         +-e
     |         |
     |         +-a
     |         +-b
     |         +-c
     |         +-d
     |         +-e
     |
     +-branch3-+-branch1-+-a
               |         +-b
               |         +-c
               |         +-d
               |         +-e
               |
               +-a
               +-b
               +-c
               +-d
               +-e
"""

__test__ = {"test_print_tree": test_print_tree}

def suite():
    suite = unittest.makeSuite(TreeTest,'test') 
    suite.addTest(doctest.DocTestSuite())
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

