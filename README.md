# Build a recipe site, a recipinator if you will

## Dev env

### Setup

* https://github.com/nvm-sh/nvm#installing-and-updating
* https://linuxize.com/post/how-to-install-node-js-on-ubuntu-22-04/
* https://www.freecodecamp.org/news/how-to-build-a-react-app-different-ways/#what-is-vite

Install nvm and node:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm -v
nvm list-remote
nvm install node
node -v
```

Install dependencies:

```bash
npm install
```

### Run

```bash
# python backend
workon py311
pip install fastapi
pip install "uvicorn[standard]"
cd backend/
uvicorn main:app --reload

# react frontend
cd frontend/
npm run dev
```
