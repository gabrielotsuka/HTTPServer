from tornado import web, ioloop, iostream, gen

class FileDownloadHandler(web.RequestHandler):
    async def get(self, filename):
        chunk_size = 1024 * 1024 * 1 
        try:
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    try:
                        self.set_header("Content-Disposition", "attachment; filename=\"" + filename + "\"")
                        self.write(chunk)
                        await self.flush()
                    except iostream.StreamClosedError:
                        break
                    finally:
                        del chunk
                        await gen.sleep(0.000000001)
        except FileNotFoundError:
            self.write("File not found on directory")

if __name__ == "__main__":
    app = web.Application([
        (r"/([0-9a-zA-Z_.% -]+)", FileDownloadHandler)
    ])
    app.listen(8080)
    print("Application started on port 8080")
    ioloop.IOLoop.current().start()