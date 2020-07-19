function I = computeIntegral(mat)


model = createpde() ;
g=decsg(mat);
geometryFromEdges(model,g); % geometryFromEdges for 2-D


edges = [2:1:(size(mat)-1)/2];
%Conditions de bord :
%Les murs non chauffés sont é la température éxterieure To = 10C
applyBoundaryCondition(model,'dirichlet','Edge',edges,'u',10);

%Le mur chauffé est modelisé par un flux rentrant , on suppose que l'on a
%mis un radiateur au niveau du mur
applyBoundaryCondition(model,'neumann','Edge',[1],'q',0,'g',10000);

a = 0;
c=1;
a=0;
f=0;
[u,p,e,t] = adaptmesh(g,model,c,a,f,'Par',0.1,'MesherVersion','R2013a');



%Le résultat est ainsi renvoyé
%On calcule l'intégrale de la fonction renvoyée

coord = p ; % Contient les coordonnées des sommets
indices = t ; % Contient les références de chaque élément
val = u ;

% On va calculer l'intégrale en évaluant la valeur de la fonction sur
% chaque petit triangle

I =0 ;
area = 0 ;
for i = 1:length(indices) ; % Pour chaque triangle
    a = coord(:,indices(1,i)) ;     % Coord du 1er point
    b = coord(:,indices(2,i)) ;     % Coord du second point
    c = coord(:,indices(3,i)) ;     % Coorddu troisi�me point

    moy = (val(indices(1,i))+val(indices(1,i))+val(indices(1,i)))/3 ;
    area = area + 0.5*abs(a(1)*c(2)-a(1)*b(2)+b(1)*a(2)-b(1)*c(2)+c(1)*b(2)-c(1)*a(2)) ;
    I = I + moy*0.5*abs(a(1)*c(2)-a(1)*b(2)+b(1)*a(2)-b(1)*c(2)+c(1)*b(2)-c(1)*a(2)) ;
end
    I = I/area ;
