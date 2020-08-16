import { COUNT_PER_PAGE } from "../config/const";

export async function getIdPaths(getIdListFn, fallback = false) {
  const idList = await recFetchIdList(getIdListFn);

  const paths = idList.map((id) => {
    return {
      params: {
        id,
      },
    };
  });

  return {
    paths,
    fallback,
  };
}

export async function getAllChildrenPagePaths(
  getAllParentFn,
  getListFn,
  countPerPage = COUNT_PER_PAGE,
  fallback = false
) {
  console.log("getAllChildrenPagePath");
  let parentIdList = await recFetchIdList(getAllParentFn);

  let cnt = 0; // For debug

  // Use resuce to fetch data sequentially, to wait
  const allPathes = await parentIdList.reduce(async (memo, parentId) => {
    await memo;
    const results = await getChildrenPagePaths(parentId, getListFn, countPerPage, fallback);
    await delay(50);
    console.log((cnt += 1));
    return [...(await memo), results];
  }, []);

  //
  const flatAllPaths = allPathes
    .map((oneParantePaths) => oneParantePaths.paths)
    .flat();

  return {
    paths: flatAllPaths,
    fallback,
  };
}

export async function getChildrenPagePaths(
  parentId,
  getListFn,
  countPerPage = COUNT_PER_PAGE,
  fallback = false,
) {
  const resultList = await recFetchList(getListFn, parentId);

  const pages = rangeArray(Math.ceil(resultList.length / countPerPage));
  const paths = pages.map((page) => ({
    params: {
      id: parentId,
      page: `${page}`,
    },
  }));

  return {
    paths,
    fallback,
  };
}

export async function getPagePaths(
    getIdListFn,
    countPerPage = COUNT_PER_PAGE,
    fallback = false
) {
  const resultList = await recFetchIdList(getIdListFn);

  const pages = rangeArray(Math.ceil(resultList.length / countPerPage));
  const paths = pages.map((page) => ({
    params: {
      page: `${page}`,
    },
  }));

  return {
    paths,
    fallback,
  };
}

export async function recFetchIdList(fn, offset = 0, totalIdList = []) {
  const { id_list: idList, next_offset: nextOffset } = await fn(offset);

  if (nextOffset < 0) {
    return totalIdList.concat(idList);
  }
  await delay(100);
  return await recFetchIdList(fn, nextOffset, totalIdList.concat(idList));
}

export async function recFetchList(fn, id, offset = 0, totalList = []) {
  const res = await fn(id, offset);
  // console.log('recFetchList')

  const { children_list: resultList, children_next_offset: nextOffset } = res;
  // console.log(await fn(id, offset))
  // console.log({resultList})
  // console.log({nextOffset})
  if (!nextOffset || nextOffset < 0) {
    // console.log(totalList)

    return totalList.concat(resultList);
  }
  await delay(100);
  return await recFetchList(fn, id, nextOffset, totalList.concat(resultList));
}

export function rangeArray(length) {
  return Array.from({ length }, (_, i) => i + 1);
}

export async function delay(t) {
  return new Promise((resolve) => setTimeout(resolve, t));
}

export function pickRandomData(idList, router) {
  const picked = idList[Math.floor(Math.random() * idList.length)];

  router.push("/fake_quotes/[id]", `/fake_quotes/${picked}`, {
    getStaticProps: true,
  });
}
