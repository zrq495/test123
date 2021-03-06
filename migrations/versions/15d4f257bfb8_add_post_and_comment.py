"""add post and comment

Revision ID: 15d4f257bfb8
Revises: 8b78ab6747b2
Create Date: 2017-08-06 17:49:55.860097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15d4f257bfb8'
down_revision = '8b78ab6747b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=16), server_default='draft', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_created_at'), 'comment', ['created_at'], unique=False)
    op.create_index(op.f('ix_comment_post_id'), 'comment', ['post_id'], unique=False)
    op.create_index(op.f('ix_comment_status'), 'comment', ['status'], unique=False)
    op.create_index(op.f('ix_comment_user_id'), 'comment', ['user_id'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=16), server_default='draft', nullable=False),
    sa.Column('published_at', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_created_at'), 'post', ['created_at'], unique=False)
    op.create_index(op.f('ix_post_published_at'), 'post', ['published_at'], unique=False)
    op.create_index(op.f('ix_post_status'), 'post', ['status'], unique=False)
    op.create_index(op.f('ix_post_user_id'), 'post', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_user_id'), table_name='post')
    op.drop_index(op.f('ix_post_status'), table_name='post')
    op.drop_index(op.f('ix_post_published_at'), table_name='post')
    op.drop_index(op.f('ix_post_created_at'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_comment_user_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_status'), table_name='comment')
    op.drop_index(op.f('ix_comment_post_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_created_at'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###
