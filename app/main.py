from fastapi import FastAPI, HTTPException
from typing import List
from .schemas import Post, Comment, UserStat, User
from .db import posts_collection, comments_collection, users_collection


app = FastAPI()


@app.get("/posts", response_model=List[Post])
def get_posts():
    posts = list(posts_collection.find({}, {"_id": 0}))
    return posts


@app.get("/comments", response_model=List[Comment])
def get_comments():
    comments = list(comments_collection.find({}, {"_id": 0}))
    return comments


@app.get("/users", response_model=List[User])
def get_users():
    comments = list(users_collection.find({}, {"_id": 0}))
    return comments


@app.get("/users/{user_id}/stats", response_model=UserStat)
def get_single_user_stats(user_id: int):
    """Get user stat for a user

    Args:
        user_id (int): user id

    Raises:
        HTTPException: when user is not found

    Returns:
        UserStat: user stat of a user
    """
    user = users_collection.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    total_posts = posts_collection.count_documents({"userId": user_id})
    total_comments = comments_collection.count_documents(
        {
            "postId": {
                "$in": [
                    post["id"] for post in posts_collection.find({"userId": user_id})
                ]
            }
        }
    )
    return UserStat(
        userId=user_id, total_posts=total_posts, total_comments=total_comments
    )


@app.get("/users/stats", response_model=List[UserStat])
def get_user_stats():
    """Get user stats for all users

    Raises:
        HTTPException: when there is an internal error

    Returns:
        List[UserStat]: list of user stats
    """
    try:
        user_stats = list(
            posts_collection.aggregate(
                [
                    {
                        "$lookup": {
                            "from": "comments",
                            "localField": "id",  # Post ID
                            "foreignField": "postId",  # Corresponding comment post ID
                            "as": "comments",
                        }
                    },
                    {
                        "$group": {
                            "_id": "$userId",
                            "total_posts": {"$sum": 1},
                            "total_comments": {"$sum": {"$size": "$comments"}},
                        }
                    },
                    {
                        "$project": {
                            "userId": "$_id",
                            "total_posts": 1,
                            "total_comments": 1,
                        }
                    },
                ]
            )
        )

        return user_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
