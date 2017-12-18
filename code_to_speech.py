import re

from gtts import gTTS

# with open('toothbrush.py') as f:
#   text = f.read()

# text = 'import sys, tty, termios, subprocess, os, json, glob, time, re'

# text = 'DIR_PATH_NOTES = os.path.expanduser("~/Dropbox/tbrush_notes")'

text = '''
def main_loop():
  # Wait for a key, build up the query string.

  if not os.path.exists(DIR_PATH_META):
    os.mkdir(DIR_PATH_META)

  start_time = time.time()
  notes = Notes()
  query_string = ' '.join(sys.argv[1:])
  query_path = os.path.join(DIR_PATH_META, 'saved_query.txt')
  if not query_string.strip() and os.path.exists(query_path):
    with open(query_path) as f:
      query_string = f.read()
  load_times_path = os.path.join(DIR_PATH_META, 'load_times.txt')
  with open(load_times_path, 'a') as f:
    f.write('{}\n'.format(time.time() - start_time))
'''

def transform_text(text):
  trans_text = text
  for find, repl in [
    ['_', ' '], ['json', 'jason'], ['usr', 'user'], ['sys', 'sis'],
    ['import', 'click import'], [r'\bdir\b', 'dirr'], ['stdin', 'standard in'],
    ['cset', ' set '], ['cget', ' get '], [r'attr\b', 'atter'],
    [r'\.([^\s])', ' dot \g<1>'],
    ['\(', ', '], ['setraw', 'set raw'], ['fileno', 'file no'], ['#+', 'hash. '],
    ['mkdir', 'make dirr'], ['argv', 'arg v'], ["' '", 'space'],
    [r'$', ', end'], [r'\b-\b', ' minus '],
  ]:
    trans_text = re.sub(find, repl, trans_text, flags=re.IGNORECASE|re.MULTILINE)

  trans_lines = [count_initial_spaces(line) for line in trans_text.splitlines()]
  return '\n'.join(trans_lines)

def count_initial_spaces(line):
  match = re.search('^ +', line)
  if match:
    return '{} {}'.format(len(match.group()), line.lstrip())
  return line

if __name__ == '__main__':
  trans_text = transform_text(text)
  print 'trans_text:', trans_text
  tts = gTTS(text=trans_text, lang='en', slow=True)
  tts.save("toothbrush.mp3")
