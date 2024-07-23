from newspaper import Article
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from background_task import background
from . models import Articles

from . webHookutils import webhook_article

@background(schedule=60)
def links_task(request,user):
    links = Articles.objects.filter(owner=user).all()
    articles_content_data = []
    payload_data = []
    try:
        for link in links:
            articles = Article(link.Article_links)
            
            articles.download()
                
            articles.parse()
                
            articles.download('punkt')
                
            articles.nlp()
            title = articles.title
            image = articles.top_image
            source = articles.source_url
            summary = articles.summary
            date_pub = articles.publish_date
            articles_content  = articles.text
                
            email_body_content = f"""
                                        <html>
                                        <head>
                                        <style>
                                        .gaga {{
                                            width: 100%;
                                        text-align: justify;
                                        margin-bottom: 10;
                                        }}
                                        hr.divider {{
                                        border-top: 1px dashed blue;
                                                }}
                                        </style>
                                        </head>
                                        <body>
                                            <div class="gaga">
                                                <h3>{title}</h3>
                                            
                                                <img src="{image}" alt="Image" style="max-width: 80%; height: auto;">
                                                <p><strong>Summary:</strong></p>
                                                <p>{summary}</p>
                                                <p><strong>Category:</strong></p>
                                                <p>{source}</p>
                                                <hr class="divider"/>
                                            </div>
                                        </body>
                                        </html>
                                        """
            payload = {
                        "title":title,
                        "image":image,
                        "source":source,
                        "content": articles_content,
                        "summary":summary, 
                        "owner":request.user.email
                    }
            
            #webhook_article(payload)
             
            articles_content_data.append(email_body_content)
            
            
        contents =''.join([str(v) for v in articles_content_data])
                
        email = EmailMessage(subject="From Content Data ",
                                    body=contents,
                                    from_email=settings.EMAIL_HOST_USER,
                                    to=[request.user.email]
                                    )
        email.content_subtype = "html" 
        res = email.send() 
    except Exception as e:
        print("error:",e)
        pass
        
    return 