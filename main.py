from Walker import Walker

def main():
    walker = Walker("config.yaml")

    walker.walk_dir()

if __name__ == "__main__":
    main()
