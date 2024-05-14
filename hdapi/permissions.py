from rest_framework.permissions import BasePermission



class IsAssociatedSiteOwnerOrProfileOwner(BasePermission):
    """
    Checks if the user owns the site or profile associated with the URL parameters.
    """

    def has_permission(self, request, view):
        associated_site_id = request.user.associated_site_id       
        
        site_id = view.kwargs.get('site_pk')
        if site_id:
            site_id = int(site_id)
        profile_id = view.kwargs.get('profile_pk')
        if profile_id:
            profile_id = int(profile_id)
        site = view.kwargs.get('site')
        if site:
            site = int(site)
        profile = view.kwargs.get('profile')
        if profile:
            profile = int(profile)       
      
        
        # Return True if neither site_pk nor profile_pk is present in the URL
        if not site_id and not profile_id and not site and not profile: 
            return True

        # If either site_pk or profile_pk exists, check ownership
        if (
            site_id == associated_site_id 
            or 
            profile_id == associated_site_id 
            or 
            site == associated_site_id 
            or 
            profile == associated_site_id
            ):
    
            return True

        return False