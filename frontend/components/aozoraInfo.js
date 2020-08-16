import RelatedInfo from './relatedInfo'

export default function AozoraInfo({
  　book
}) {
  return (
    <RelatedInfo>
      <a href={book.url} target="_blank" rel="noopener noreferrer">
        青空文庫『{book.title}』
      </a>
    </RelatedInfo>
  );
}
