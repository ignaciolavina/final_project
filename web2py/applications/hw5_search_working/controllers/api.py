
# Retrieves the user in case of be logged
def get_logged_in_user():
    user = None if auth.user is None else auth.user.email
    return response.json(dict(user=user))

# function called at the beggining of the page display
# It retrieves all the list of products, and computes on the server side the average rating
def get_all_products():
    products = db(db.product).select()
    for product in products:
        product.avg_rating = 0
        sum = 0
        reviews = db((db.review.product_id == product.id) & (db.review.rating > 0)).select()
        # Average rating computation:
        for review in reviews:
            sum += review.rating
        if (len(reviews) != 0):
            product.avg_rating = sum / len(reviews)        

    return response.json(dict(products=products))

# To get the user review, we require the user to be logged in order to detect wich user review we have to retrieve
@auth.requires_login()
def get_your_review():
    review = db((db.review.product_id == request.vars.product_id) & (db.review.email == request.vars.email)).select().first()
    return response.json(dict(review=review))

# Function that allows to store on the database the review sended from the client side
# for that we retrieve the parameters of the request
@auth.requires_login()
def save_review():
    print(request.vars.product_id)
    print(request.vars.email)
    db.review.update_or_insert(
        ((db.review.product_id == request.vars.product_id) & (db.review.email == request.vars.email)),
        body=request.vars.body,
        product_id=request.vars.product_id
    )
    return "ok"

# Method that allows send to the client all the reviews of an specific product (known by the request vars)
def get_other_reviews():
    if auth.user is None:
        other_reviews = db(db.review.product_id == request.vars.product_id).select()
    else:
        other_reviews = db( (db.review.product_id == request.vars.product_id) & (db.review.email != auth.user.email) ).select()    
    return response.json(dict(other_reviews=other_reviews))

# method for updating the star rating of an specific user (thats why we require autentification)
@auth.requires_login()
def update_star():
    db.review.update_or_insert(
        ((db.review.product_id == request.vars.product_id) & (db.review.email == request.vars.email)),
        rating=request.vars.rating,
        product_id=request.vars.product_id
    )
    # db.product.update_or_insert(
    #     db(db.review.product_id == request.vars.product_id).select()
    #     book.avg_rating = request.vars.avg_rating
    # )
    return "ok"


# Method that receives trhough the request vars an string that the user has input on the search var
# And retrieves only the products that match part of that string
def search():
    products = db(db.product).select()
    # Obtaining the string of the search var from the request vars
    s = request.vars.search_string or ''
    # list of products to send back from the server
    res = []
    # Iterating thouth all the products
    for p in products:
        # if the string is in the product name (upper & lower case match)
        if s.lower() in p.name.lower():
            # Then add to the list "res" to send back
            res.append(p)

    return response.json(dict(products_shown=res))