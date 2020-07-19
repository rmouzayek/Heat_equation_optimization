function I = Integrale(u)
%INTEGRALTRIANGLE renvoie une valeur approchée de l'intégrale 
coord = u.p ; % Contient les coordonnées des sommets 
indices = u.t ; % Contient les références de chaque élément
val = u.u ; 

% On va calculer l'intégrale en évaluant la valeur de la fonction sur
% chaque petit triangle 

I =0 ; 
area = 0 ; 
for i = 1:length(indices) ; % Pour chaque triangle 
    a = coord(:,indices(1,i)) ;     % Coord du 1er point 
    b = coord(:,indices(2,i)) ;     % Coord du second point 
    c = coord(:,indices(3,i)) ;     % Coorddu troisième point
    
    moy = (val(indices(1,i))+val(indices(1,i))+val(indices(1,i)))/3 ;
    area = area + 0.5*abs(a(1)*c(2)-a(1)*b(2)+b(1)*a(2)-b(1)*c(2)+c(1)*b(2)-c(1)*a(2)) ; 
    I = I + moy*0.5*abs(a(1)*c(2)-a(1)*b(2)+b(1)*a(2)-b(1)*c(2)+c(1)*b(2)-c(1)*a(2)) ;
end
    I = I/area ; 
end

