from rest_framework.viewsets import ModelViewSet
from .serializer import Product_Serializer
from .models import Products
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import MessagesPlaceholder



class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = Product_Serializer

llm = ChatOllama(model="llama3.2")
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful product-support assistant.\n"
     "You only know about the following products for this user:\n"
     "{product_info}\n"
     "Never invent other products or versions not listed above.\n"
     "If the user asks about 'my product' and there is only ONE product, "
     "answer with the product's **status** (e.g., shipped, processing) and category if relevant.\n"
     "If there are MULTIPLE products and the user is unclear, ask them to specify which one.\n"
     "Never reveal details about products of other customers.\n"
     "Keep responses short and factual."),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])

converstation = []

class BotView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_question = request.data.get("input", "")
        user_product = Products.objects.filter(customer_name = request.user)
        if not user_product.exists():
            return Response({"answer":"You have no orders."})
        # product_info = Product_Serializer(user_product, many=True).data
        product_info = "\n".join(
            [f"customer_name :{p.customer_name}, product_name:{p.product_name}, category:{p.category},status:{p.status},price:{p.price}"
             for p in user_product]
        )

        converstation.append(HumanMessage(content=user_question))

        chain = template | llm | StrOutputParser()
        
        res = chain.invoke({
            "input":user_question,
            "history":converstation,
            "product_info":product_info})
        converstation.append(AIMessage(content=res))
        return Response({"answer":res})