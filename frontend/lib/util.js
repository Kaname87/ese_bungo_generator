import {
    recFetchIdList
} from './api'


export async function getIdPaths(getIdListfn, fallback=false) {
 const idList = await recFetchIdList(getIdListfn)

 const paths = idList.map(id => {
   return {
     params: {
       id,
     }
   }
 });

 return {
   paths,
   fallback,
 }
}