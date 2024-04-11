kill:
	cd backend && docker stop playlify_container

clean:
	cd backend && docker rm playlify_container
	docker rmi playlify:latest

build:
	cd backend && docker build -t playlify . # Build images

start:
	cd backend && docker run -p 5000:5000 --name playlify_container -t playlify

restart:
	cd backend && docker start playlify_container

prune:
	cd backend && docker system prune
