export const COUNT_PER_PAGE_AUTHOR = 10;
export const COUNT_PER_PAGE = 10;
export const CHILDREN_MAX_DISPLAY = 3;

export const SITE_NAME = 'エセ文豪文庫'
export const SITE_URL = `${process.env.SITE_URL}`
export const API_BASE_URL = `${process.env.API_BASE_URL}`

export const PROFILE_IMAGE_LIST = [
    "/images/profile/hayashi.jpg",
    "/images/profile/fuyume.jpg",
    "/images/profile/akutako.jpg",
]

export const TOP_PAGE_FAKE_QUOTE_ID = `${process.env.TOP_PAGE_FAKE_QUOTE_ID}`

export const NOT_FOUND_DATA = {
  fakeQuote: {
    text:
      '申し訳ありません。貴女が直接アクセスした頁は、除外されたか、Webページが変更しされているとき省略することができません',
  },
  fakeBook: {
    title: '頁が見つかりませんでした',
  },
  fakeAuthor: {
    name: 'ソーシャル・ネットワーキング・サービス経営者',
  },
  quote: {
    text:
      '申し訳ありません。あなたがアクセスしたページは、削除されたか、URLが変更されているため表示することができません',
  },
  book: {
    title: 'ページが見つかりませんでした',
  },
  author: {
    name: 'サイト運営者',
  },
};

// 使わんかも
export const ERROR_DATA = {
    fakeQuote: {
      text:
        '例外処理により巻末が掲出ができません',
    },
    fakeBook: {
      title: '巻末が掲出ができません',
    },
    fakeAuthor: {
      name: 'ソーシャル・ネットワーキング・サービス経営者',
    },
    quote: {
      text:
        '申し訳ありません。エラーによりページが表示ができません',
    },
    book: {
      title: 'ページが表示できません',
    },
    author: {
      name: 'サイト運営者',
    },
  };
