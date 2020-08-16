import Pager from "./pager";

export default function PagerWrapper({
  children,
  page,
  total,
  perPage,
  href,
  asCallback,
}) {
  return (
    <div>
      <Pager
        page={page}
        total={total}
        perPage={perPage}
        href={href}
        asCallback={asCallback}
      />
      <div>{children}</div>
      <Pager
        page={page}
        total={total}
        perPage={perPage}
        href={href}
        asCallback={asCallback}
      />
    </div>
  );
}
