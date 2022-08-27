from app import oauth2
from .. import models, oauth2
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..schemas import Post,PostCreate,PostOut
from typing import List,Optional
from ..database import engine,get_db
from sqlalchemy import func

router =APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int =10, skip:int =0, search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Post)
def create_posts(posts: PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # print(post)
    # print(post.dict())
    # post_dict  = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(posts.title,posts.content,posts.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(owner_id=current_user.id,**posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    #print(test_post)
    # post = find_post(id)
    post_query = db.query(models.Post).filter(models.Post.id== id)

    post  = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id== id).first()
 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    #     # response.status_code=status.HTTP_404_NOT_FOUND
    #     # return {"message":f"post with id {id} was not found"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int ,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    #index =find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id== id)

    post  = post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to performed the requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    #my_posts.pop(index)
    #conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=Post)
def update_posts(id: int,posts: PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # index =find_index_post(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s  RETURNING *""",(posts.title,posts.content,posts.published,str(id)))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id== id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to performed the requested action")


    post_query.update(posts.dict(),synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = 
    #conn.commit()
    return post