import inotify.adapters

def main():
  i = inotify.adapters.Inotify()

  i.add_watch('./temp')

  for event in i.event_gen(yield_nones=False):
    (_, type_names, path, filename) = event

    print(f'Path [{path}] Filename=[{filename}] Types=[{type_names}]')

if __name__ == '__main__':
  main()