import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('login', sa.String, nullable=False, unique=True),
    sa.Column('name', sa.String, nullable=False)
)

stats = sa.Table(
    'stats',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),  # TODO add comments on altering repo_id to id
    sa.Column('user_id', sa.BigInteger, sa.ForeignKey('user.id'), nullable=False),  # TODO add cascade
    sa.Column('repo_id', sa.BigInteger, nullable=False),  # TODO add comments on altering repo_id to id
    sa.Column('date', sa.Date, nullable=False),
    sa.Column('stargazers', sa.Integer, nullable=False),
    sa.Column('forks', sa.Integer, nullable=False),
    sa.Column('watchers', sa.Integer, nullable=False)
)
