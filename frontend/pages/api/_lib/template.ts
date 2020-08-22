function getCss() {
  return `
  @font-face {
    font-family: 錦明朝;
    src: url("./nishiki.otf") format("opentype");
}
html,body {
  font-size: 16px;
  background-image: url("https://esebunko.vercel.app/images/whitepaper.jpg");
  color: #000;
  font-family: 錦明朝;
  margin: 0 auto;
}
body a {
    color: #000;
}
* {
  box-sizing: border-box;
}
img {
  max-width: 100%;
  display: block;
}
.container {
  margin-top: 1.5rem;
  padding: 0 7%;
}
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  text-align: center;
  padding-bottom: 10px;
}
.main h1 {
  font-weight: 100;
  font-size: 1.5rem;
  color: $important-color;
}
.main li {
  list-style-type: none;
}

.header {
  width: 100%;
  margin: 4% 0 2% 0;
}
.serviceNameWrapper {
  display: flex;
  justify-content: space-between;
  vertical-align: middle;
}
.serviceName {
  font-size: 1rem;
  margin: auto;
}

.fake {
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex-wrap: nowrap;
  margin: 0 5%;
}
.fakeAuthorWrapper {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  min-width: 40%;
  max-width: 40%;
  padding: 2%;
}
.fakeAuthor {
  flex-grow: 1;
  margin: 2% 5% 5% 5%;
}
.profile {
  min-width: 100%;
  object-fit: contain;
}
.novel {
  justify-content: flex-start;
  margin: auto;
  flex-grow: 3;
}
.random {
  flex-grow: 1;
  color: transparent;
  width: 25%;
  font-size: 0.6rem;
  color: #f8f6f5;
  display: none;
}
.fakeQuote {
  margin: 0 5%;
  padding: 3%;
  font-size: 1.3rem;
}
.fakeCite {
  margin-left: auto;
  text-align: right;
  margin: 5% 0 2% 0;
  font-size: 1.1rem;
}
.fakeCite a {
  text-decoration: none;
  color: #000;
  border-bottom: .05px solid #000;
}
.fakeAuthorName {
  margin-right: 5px;
}
.originalInfo {
  margin: 2% 3%;
  padding: 0 2%;
}
.originalInfo blockquote {
  border-top: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 3% 3%;
}
.originalInfo blockquote a{
  color: #666;
}
.originalInfo p,
.originalInfo a {
  padding: 0;
  margin: 0 0 3% 0;
  line-height: 1.7;
}
.originalInfo cite {
  display: block;
  text-align: right;
  font-size: 0.9rem;
}
.originalInfo cite {
  display: block;
  text-align: right;
  font-size: 0.9rem;
}

.originalQuote {
  font-size: 1.2rem;
  text-decoration: none;
}
.originalCite {
  margin-top: 20px;
  font-size: 1.2rem;
}
.originalCite a:first-child{
  margin-right: 3px;
}
`;
}

export function getHtml(parsedReq: ParsedRequest) {
  const {
    author = "太宰治",
    book = "走れメロス",
    quote = "メロスは激怒した。",
    fakeAuthor = "圭宰治",
    fakeBook = "走れアンジェリカ",
    fakeQuote = "アンジェリカは激高した。",
    profileName = "hayashi",
  } = parsedReq;
  return `
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=1024, initial-scale=1">
      <title>OGP</title>
    </head>
    <style>
    ${getCss()}
    </style>
    <body>
    <div id="">
      <div class="container">
        <header class="header">
          <div class="serviceNameWrapper">
            <a class="serviceName" href="/">エセ文庫</a>
          </div>
        </header>
        <main class="main">
          <section>
            <div class="fake">
              <div class="fakeAuthorWrapper">
                <a class="random">ランダム</a>
                <div class="fakeAuthor">
                  <img src="https://esebunko.vercel.app/images/profile/${profileName}.jpg" alt="エセ文豪著者近影"/>
                </div>
                <a class="random">ランダム</a>
              </div>
              <div class="novel">
                <p class="fakeQuote">${fakeQuote}</p>
                <p class="fakeCite">
                  <span>
                    <a class="fakeAuthorName">${fakeAuthor}</a>
                    <a>『${fakeBook}』</a>
                  </span>
                </p>
              </div>
            </div>
            <div class="originalInfo">
              <blockquote>
                <a class="originalQuote">${quote}</a>
                <cite class="originalCite">
                  <a href="/">${author}</a>
                  <a href="/">『${book}』</a>
                </cite>
              </blockquote>
            </div>
          </section>
        </main>
      </div>
    </div>
  </html>
`;
}
