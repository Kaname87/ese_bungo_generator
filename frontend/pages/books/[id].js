// import Layout from '../../components/layout';
// // import FakeQuoteCard from '../../components/fakeQuoteCard';

// import {
//     getFakeAuthorListByAuthorId,
//     getAuthorIdList,
// } from '../../lib/api'

// import { getIdPaths } from '../../lib/util'


// export default function Author({
// //   fakeQuote,
// //   fakeBook,
//   fakeAuthorList,
//   bookList,
//   author,
// }) {
//   return (
//     <Layout>
//       <div>{author.name}</div>
//       {bookList.map(book => (
//           <div>{book.title}</div>
//       ))}
//     <hr />
//     {fakeAuthorList.map(fakeAuthor => (
//           <div>{fakeAuthor.name}</div>
//       ))}
//     </Layout>
//   )
// }

// export async function getStaticPaths() {
//   return await getIdPaths(getAuthorIdList)
// }

// export async function getStaticProps({ params }) {

//   const {
//     author,
//     book_list: bookList,
//     fake_author_list: fakeAuthorList,
//    } = await getFakeAuthorListByAuthorId(params.id)


//   return {
//     props: {
//       author,
//       bookList,
//       fakeAuthorList,
//     }
//   }
// }
