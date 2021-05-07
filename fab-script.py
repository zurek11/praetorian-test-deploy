if __name__ == '__main__':
    import sys
    from fabric.main import make_program

    path = sys.argv[:1]
    args = ' '.join(sys.argv[-6:])

    make_program().run(args)
