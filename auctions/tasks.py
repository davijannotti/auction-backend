
from celery import shared_task
from django.utils import timezone
from .models import Auction, Bid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def end_expired_auctions():
    now = timezone.now()
    expired_auctions = Auction.objects.filter(end_time__lte=now, status=Auction.Status.ATIVO.name)

    if not expired_auctions:
        return "No expired auctions to process."

    channel_layer = get_channel_layer()

    for auction in expired_auctions:
        auction.status = Auction.Status.ENCERRADO.name
        highest_bid = Bid.objects.filter(item__auction=auction).order_by('-amount').first()
        winner_info = None
        if highest_bid:
            auction.winner = highest_bid.user
            winner_info = {
                'username': highest_bid.user.username,
                'id': highest_bid.user.id
            }
        
        auction.save()

        message = {
            'type': 'auction_ended',
            'message': {
                'auction_id': auction.id,
                'winner': winner_info
            }
        }

        async_to_sync(channel_layer.group_send)(
            f'auction_{auction.id}',
            message
        )
    
    return f"Processed {len(expired_auctions)} expired auctions."
