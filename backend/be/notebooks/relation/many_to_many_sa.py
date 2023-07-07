"""SQLAlchemy Many-to-Many Relationship.

https://avacariu.me/writing/2019/composite-foreign-keys-and-many-to-many-relationships-in-sqlalchemy
"""

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Author(Base):
    __tablename__ = "author"

    first_name = Column(String, primary_key=True)
    last_name = Column(String, primary_key=True)

    articles = relationship(
        "Article",
        secondary="authorarticle",
        back_populates="authors",
    )


class Article(Base):
    __tablename__ = "article"
    slug = Column(String, primary_key=True)

    authors = relationship(
        "Author",
        secondary="authorarticle",
        back_populates="articles",
    )


class AuthorArticle(Base):
    __tablename__ = "authorarticle"

    article_slug = Column(String, ForeignKey(Article.slug), primary_key=True)
    author_first = Column(String, primary_key=True)
    author_last = Column(String, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["author_first", "author_last"],
            ["author.first_name", "author.last_name"],
        ),
    )


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session = Session()

    author = Author(first_name="Name", last_name="Surname")
    article = Article(slug="some-article")

    author.articles.append(article)

    session.add(author)
    session.add(article)
    session.commit()
