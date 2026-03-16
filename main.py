import socket,os
def s():
 b=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 b.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
 p=8080
 try:b.bind(('0.0.0.0',p))
 except:p=8081;b.bind(('0.0.0.0',p))
 b.listen(5)
 print(f"http://localhost:{p}")
 while 1:
  try:
   c,a=b.accept()
   r=c.recv(4096).decode('utf-8',errors='ignore')
   if not r:continue
   u=r.split(' ')[1].split('?')[0]
   if u=='/':u='/group.html'
   f='.'+u
   if os.path.exists(f):
    with open(f,'rb') as x:d=x.read()
    m='text/html' if f.endswith('.html') else 'application/javascript' if f.endswith('.js') else 'text/plain'
    h=f"HTTP/1.1 200 OK\r\nContent-Type: {m}\r\nContent-Length: {len(d)}\r\n\r\n".encode()
    c.sendall(h+d)
   else:c.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
   c.close()
  except:pass
if __name__=='__main__':s()
