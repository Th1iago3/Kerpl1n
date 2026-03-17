import socket,os,sys,time,datetime,threading
from pathlib import Path

def format_time():
 return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def get_local_ip():
 s_local=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 s_local.connect(('8.8.8.8',80))
 ip=s_local.getsockname()[0]
 s_local.close()
 return ip

def parse_ua(ua):
 if 'iPhone' in ua:
  if 'OS 17' in ua:return '17.x'
  elif 'OS 16' in ua:return '16.x'
  elif 'OS 15' in ua:return '15.x'
  else:return 'unknown'
 elif 'iPad' in ua:return 'iPad'
 elif 'Mac' in ua:return 'MacOS'
 return 'unknown'

def find_alt_path(base_path):
 if os.path.exists(base_path):return base_path
 for root,dirs,files in os.walk('.'):
  for f in files:
   if f in os.path.basename(base_path) or base_path.split('/')[-1] in f:
    return os.path.join(root,f)
 return None

def s():
 b=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 b.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
 p=8080
 try:b.bind(('0.0.0.0',p))
 except:p=8081;b.bind(('0.0.0.0',p))
 b.listen(5)
 ip_local=get_local_ip()
 print(f"[{format_time()}] SERVER_START|IP:{ip_local}|PORT:{p}|TIME:{datetime.datetime.now()}")
 sys.stdout.flush()
 while True:
  try:
   c,a=b.accept()
   ts=format_time()
   r=c.recv(4096).decode('utf-8',errors='ignore')
   if not r:c.close();continue
   try:
    ua_line=[l for l in r.split('\r\n') if l.startswith('User-Agent:')]
    ua=ua_line[0].replace('User-Agent: ','').strip() if ua_line else 'UNKNOWN'
   except:ua='UNKNOWN'
   device_type=parse_ua(ua)
   u=r.split(' ')[1].split('?')[0]
   if u=='/':u='/group.html'
   f='.'+u
   alt_path=None
   if os.path.exists(f):file_path=f
   else:
    alt_path=find_alt_path(f)
    if alt_path:file_path=alt_path
    else:file_path=None
   if file_path:
    try:
     with open(file_path,'rb') as x:d=x.read()
     m='text/html' if file_path.endswith('.html') else 'application/javascript' if file_path.endswith('.js') else 'text/plain'
     h=f"HTTP/1.1 200 OK\r\nContent-Type: {m}\r\nContent-Length: {len(d)}\r\n\r\n".encode()
     c.sendall(h+d)
     print(f"[{ts}] SERVE_FILE|PATH:{u}|SIZE:{len(d)}|TYPE:{m}|TO:{a[0]}|DEVICE:{device_type}|STATUS:200")
    except Exception as ex:
     c.sendall(b"HTTP/1.1 500 Internal Error\r\n\r\n")
     print(f"[{ts}] ERROR_READ|PATH:{u}|FROM:{a[0]}|ERROR:{str(ex)}")
   else:
    c.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    print(f"[{ts}] FILE_NOT_FOUND|PATH:{u}|FROM:{a[0]}|DEVICE:{device_type}|STATUS:404")
   c.close()
  except KeyboardInterrupt:
   print(f"\n[{format_time()}] SERVER_SHUTDOWN|KEYBOARD_INTERRUPT")
   b.close()
   sys.exit(0)
  except Exception as ex:
   print(f"[{format_time()}] CONN_ERROR|ERROR:{str(ex)}")
   try:c.close()
   except:pass

if __name__=='__main__':
 try:s()
 except KeyboardInterrupt:
  print(f"\n[{format_time()}] MAIN_INTERRUPT|SHUTDOWN")
