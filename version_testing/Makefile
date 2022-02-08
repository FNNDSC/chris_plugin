IMAGES := $(shell docker images -f label=org.chrisproject.test=chris_plugin -q)

test:
	$(foreach image,$(IMAGES),./test.sh $(image);)  # FIXME doesn't fail when it should

build:
	docker buildx bake --load

clean:
	docker rmi $(IMAGES)

.PHONY: clean
